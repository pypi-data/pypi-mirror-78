from datetime import datetime


def str_to_timestamp(time_str):
	return int(datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').strftime("%s"))


def timestamp_to_str(timestamp):
	return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def iso_to_str(timestamp):
	d = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
	return d.strftime("%Y-%m-%d %H:%M:%S")


def get_today_begin_timestamp():
	today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
	return int(today.strftime("%s"))
