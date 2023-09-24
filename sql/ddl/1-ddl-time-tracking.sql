
create table if not exists public.workspace (
    id varchar not null unique,
    name varchar,
	hourly_rate_amount integer,
	hourly_rate_currency varchar,
	cost_rate_amount integer,
	cost_rate_currency varchar,
	primary key(id)
);

create table if not exists public.project (
    id varchar not null unique,
    name varchar,
	hourly_rate_amount integer,
	hourly_rate_currency varchar,
	client_id varchar,
	workspace_id varchar,
	membership_id varchar,
	duration varchar,
	time_estimate varchar,
	time_estimate_type varchar,
	time_estimate_active boolean,
	billable boolean,
	archived boolean,
	public boolean,
	primary key(id),
	constraint fk_project_workspace foreign key(workspace_id) references workspace(id)
);

create table if not exists public.client (
    id varchar not null unique,
    name varchar,
	email varchar,
	workspace_id varchar,
	archived boolean,
	address varchar,
	note varchar,
	primary key(id)
);

create table if not exists public.user (
    id varchar not null unique,
    name varchar,
	email varchar,
	active_workspace varchar,
	default_workspace varchar,
	setting_week_start varchar,
	setting_week_time_zone varchar,
	setting_start_day varchar,
	status varchar,
	primary key(id)
);

create table if not exists public.task (
    id varchar not null unique,
    name varchar,
	project_id varchar,
	estimate varchar,
	duration varchar,
	billable boolean,
	hourly_rate_amount integer,
	hourly_rate_currency varchar,
	cost_rate_amout integer,
	cost_rate_currency varchar,
	primary key(id),
	constraint fk_task_project foreign key(project_id) references project(id)
);

create table if not exists public.membership (
    name varchar,
	hourly_rate_amount integer,
	hourly_rate_currency varchar,
	cost_rate_amount integer,
	cost_rate_currency varchar,
	status varchar,
	membership_type varchar,
	user_id varchar,
	workspace_id varchar,
	constraint fk_membership_user foreign key(user_id) references public.user(id),
	constraint fk_membership_workspace foreign key(workspace_id) references workspace(id)
);

create table if not exists public.time_entry (
    id varchar not null unique,
    description varchar,
	user_id varchar,
	project_id varchar,
	client_id varchar,
	time_interval_start timestamptz,
	time_interval_end timestamptz,
	time_interval_duration integer,
	billable boolean,
	amount numeric,
	cost numeric,
	profit numeric,
	rate numeric,
	primary key(id),
	constraint fk_time_entry_user foreign key(user_id) references public.user(id),
	constraint fk_time_entry_project foreign key(project_id) references project(id),
	constraint fk_time_entry_client foreign key(client_id) references client(id)
	
);