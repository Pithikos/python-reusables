import itertools
import re


def generate_all_datetime_regex():
    # Create regular expressions for matching any possible date/time
    re_time  = [
        r'\d{2}\d{2}',                                      # 0000
        r'\d{2}:\d{2}',                                     # 00:00
        r'\d{2}:\d{2}\d{2}',                                # 00:00:00
        r'\d{2}\.\d{2}',                                    # 00.00
        r'\d{2}\.\d{2}\.\d{2}',                             # 00.00.00
    ]
    re_zone = [
        r'[-+ ]\d{2}:\d{2}',                                # +01:00
        r'[\. ]\d{3}Z',                                     # .000Z
    ]
    re_dates = [
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',             # 2011-04-16T00:00:00
        r'\d{4}/\d{2}/\d{2}',                               # 2011/04/16
        r'\d{2}/\d{2}/\d{4}',                               # 4/16/2011
        r'\d{2}/\d{2}/\d{2}',                               # 11/04/16
        r'\d{4}-\d{2}-\d{2}',                               # 2011-04-16
        r'\d{2}-\d{2}-\d{4}',                               # 16-04-2011
        r'\d{2}-\d{2}-\d{2}',                               # 16-04-11
        r'\d{4}\.\d{2}\.\d{2}',                             # 2011.04.16
        r'\d{2}\.\d{2}\.\d{4}',                             # 16.04.2011
        r'\d{2}\.\d{2}\.\d{2}',                             # 16.04.11
    ]
    datezone_comb     = [d+z          for d,z  in itertools.product(re_dates, re_zone)]
    datezonetime_comb = [dz+'[T -]'+t for dz,t in itertools.product(datezone_comb, re_time)]
    timedatezone_comb = [t+'[T -]'+dz for t,dz in itertools.product(re_time, datezone_comb)]
    timedate_comb     = [t+'[T -]'+d  for t,d  in itertools.product(re_time, re_dates)]
    datetime_comb     = [d+'[T -]'+t  for d,t  in itertools.product(re_dates, re_time)]

    all_regex = datezone_comb + datezonetime_comb + timedatezone_comb + timedate_comb + datetime_comb
    all_regex.sort(key=len, reverse=True)

    return all_regex




# ----------------------------- Usage ----------------------------------

text = 'This text was written at 08/03/2016 16.30pm.'

for regex in generate_all_datetime_regex():
	found = re.search(regex, text)
	if found:
		print("Found datetime: %s" % found.group())
		
# => Found datetime: 08/03/2016 16.30
