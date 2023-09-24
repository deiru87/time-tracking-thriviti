
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
	primary key(id)
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
	primary key(id)
);

create table if not exists public.membership (
	hourly_rate_amount integer,
	hourly_rate_currency varchar,
	cost_rate_amount integer,
	cost_rate_currency varchar,
	status varchar,
	membership_type varchar,
	user_id varchar,
	workspace_id varchar
);

create table if not exists public.time_entry (
    id varchar not null unique,
    description varchar,
	user_id varchar,
	project_id varchar,
	client_id varchar,
	time_interval_start timestamp with time zone UTC DEFAULT now(),
	time_interval_end  timestamp with time zone UTC DEFAULT now(),
	time_interval_duration integer,
	billable boolean,
	amount numeric,
	cost numeric,
	profit numeric,
	rate numeric,
	primary key(id)
	
);

create view consolidated as 
	select 
	(select name from project where id = t.project_id) as project_name,
	(select name from client where id = t.client_id) as client_name,
	date_trunc('DAY', t.time_interval_end) as date,
	t.project_id,
	sum(t.time_interval_duration/60) as duration_in_min,
	sum(t.amount) as amount,
	sum(t.cost) as cost,
	sum(t.profit) as profit
	from time_entry t
	group by t.project_id, t.client_id, date_trunc('DAY', t.time_interval_end)
	order by date desc;