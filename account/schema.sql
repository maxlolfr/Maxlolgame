-- Maxlol Games — compte joueur universel (Supabase / Postgres). Toutes les tables sont protégées par RLS.
-- Les achats/licences restent côté serveur de paiement (secrets PayPal) ; ici : profil, sauvegardes, appareils.

create table if not exists public.profiles (
  id uuid primary key,                       -- = auth.users.id
  display_name text check (char_length(display_name) <= 40),
  created_at timestamptz not null default now()
);

-- Une ligne = un emplacement de sauvegarde d'un jeu. "version" sert à détecter les conflits (jamais d'écrasement silencieux).
create table if not exists public.saves (
  user_id uuid not null,
  game text not null check (game ~ '^[a-z0-9-]{2,40}$'),
  slot text not null default 'main' check (slot ~ '^[a-z0-9-]{1,20}$'),
  version int not null default 1,
  data jsonb not null,
  size_bytes int not null,
  device_id text,
  updated_at timestamptz not null default now(),
  primary key (user_id, game, slot)
);

-- Historique : les 5 dernières versions remplacées sont conservées (annulation possible).
create table if not exists public.save_history (
  id bigint generated always as identity primary key,
  user_id uuid not null, game text not null, slot text not null,
  version int not null, data jsonb not null, device_id text,
  replaced_at timestamptz not null default now()
);
create index if not exists save_history_idx on public.save_history (user_id, game, slot, replaced_at desc);

alter table public.profiles enable row level security;
alter table public.saves enable row level security;
alter table public.save_history enable row level security;

-- Lecture seule directe de ses propres données ; AUCUNE écriture directe sur saves (tout passe par les fonctions ci-dessous).
create policy profiles_own_select on public.profiles for select using (id = auth.uid());
create policy profiles_own_update on public.profiles for update using (id = auth.uid()) with check (id = auth.uid());
create policy saves_own_select on public.saves for select using (user_id = auth.uid());
create policy hist_own_select on public.save_history for select using (user_id = auth.uid());
revoke insert, update, delete on public.saves, public.save_history from anon, authenticated;
revoke all on public.saves, public.save_history, public.profiles from anon;

-- Création automatique du profil à l'inscription
create or replace function public.handle_new_user() returns trigger language plpgsql security definer set search_path = public as $$
begin insert into public.profiles (id) values (new.id) on conflict do nothing; return new; end $$;

-- Écriture d'une sauvegarde avec contrôle de version.
-- p_base_version = version que le client croit avoir (0 = rien dans le cloud).
-- Si le cloud a changé entre-temps => statut 'conflict' et RIEN n'est écrit ; le client doit demander à l'utilisateur.
create or replace function public.put_save(p_game text, p_slot text, p_base_version int, p_data jsonb, p_device text default null)
returns jsonb language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); cur public.saves; sz int := octet_length(p_data::text);
begin
  if uid is null then raise exception 'not_authenticated' using errcode = '28000'; end if;
  if sz > 262144 then return jsonb_build_object('status','too_large','max',262144); end if;   -- 256 Ko max par sauvegarde
  select * into cur from public.saves where user_id = uid and game = p_game and slot = p_slot for update;
  if not found then
    if p_base_version <> 0 then return jsonb_build_object('status','conflict','cloud_version',0); end if;
    insert into public.saves (user_id, game, slot, version, data, size_bytes, device_id) values (uid, p_game, p_slot, 1, p_data, sz, p_device);
    return jsonb_build_object('status','ok','version',1);
  end if;
  if cur.version <> p_base_version then
    return jsonb_build_object('status','conflict','cloud_version',cur.version,'cloud_updated_at',cur.updated_at,'cloud_device',cur.device_id);
  end if;
  insert into public.save_history (user_id, game, slot, version, data, device_id) values (uid, p_game, p_slot, cur.version, cur.data, cur.device_id);
  delete from public.save_history where id in (select id from public.save_history where user_id = uid and game = p_game and slot = p_slot order by replaced_at desc, id desc offset 5);
  update public.saves set version = cur.version + 1, data = p_data, size_bytes = sz, device_id = p_device, updated_at = now() where user_id = uid and game = p_game and slot = p_slot;
  return jsonb_build_object('status','ok','version',cur.version + 1);
end $$;

-- Restaure une ancienne version : la version courante part elle-même dans l'historique (rien n'est jamais perdu).
create or replace function public.restore_save(p_game text, p_slot text, p_history_id bigint)
returns jsonb language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid(); h public.save_history; cur public.saves;
begin
  if uid is null then raise exception 'not_authenticated' using errcode = '28000'; end if;
  select * into h from public.save_history where id = p_history_id and user_id = uid and game = p_game and slot = p_slot;
  select * into cur from public.saves where user_id = uid and game = p_game and slot = p_slot for update;
  if h.id is null or cur.user_id is null then return jsonb_build_object('status','not_found'); end if;
  insert into public.save_history (user_id, game, slot, version, data, device_id) values (uid, p_game, p_slot, cur.version, cur.data, cur.device_id);
  update public.saves set version = cur.version + 1, data = h.data, size_bytes = octet_length(h.data::text), updated_at = now() where user_id = uid and game = p_game and slot = p_slot;
  return jsonb_build_object('status','ok','version',cur.version + 1);
end $$;

-- Export RGPD : toutes les données personnelles stockées ici, en un JSON.
create or replace function public.export_my_data() returns jsonb language sql security definer set search_path = public as $$
  select jsonb_build_object('exported_at', now(), 'user_id', auth.uid(),
    'profile', (select to_jsonb(p) from public.profiles p where p.id = auth.uid()),
    'saves', coalesce((select jsonb_agg(to_jsonb(s)) from public.saves s where s.user_id = auth.uid()), '[]'::jsonb),
    'save_history', coalesce((select jsonb_agg(to_jsonb(h)) from public.save_history h where h.user_id = auth.uid()), '[]'::jsonb));
$$;

-- Suppression des données de jeu (la suppression du compte d'authentification lui-même passe par la fonction serveur, cf. architecture).
create or replace function public.delete_my_game_data() returns jsonb language plpgsql security definer set search_path = public as $$
declare uid uuid := auth.uid();
begin
  if uid is null then raise exception 'not_authenticated' using errcode = '28000'; end if;
  delete from public.save_history where user_id = uid; delete from public.saves where user_id = uid; delete from public.profiles where id = uid;
  return jsonb_build_object('status','ok');
end $$;

revoke all on function public.put_save(text,text,int,jsonb,text), public.restore_save(text,text,bigint), public.export_my_data(), public.delete_my_game_data() from public, anon;
grant execute on function public.put_save(text,text,int,jsonb,text), public.restore_save(text,text,bigint), public.export_my_data(), public.delete_my_game_data() to authenticated;

-- Profil créé automatiquement à l'inscription (Supabase uniquement : le schéma auth existe)
do $$ begin
  if to_regclass('auth.users') is not null then
    drop trigger if exists on_auth_user_created on auth.users;
    create trigger on_auth_user_created after insert on auth.users for each row execute function public.handle_new_user();
  end if;
end $$;
