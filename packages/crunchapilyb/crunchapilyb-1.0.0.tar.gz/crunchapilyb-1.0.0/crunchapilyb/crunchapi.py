from .records import get_records


# API to search people.
def crunch_api_ppl(num_records=-1, since_time=None, sort_order=None,
                   name=None, query=None, locations=None, types=None,
                   socials=None, csv_name=None):
    df = get_records(0, since_time=since_time, name=name, query=query,
                     sort_order=sort_order, locations=locations,
                     types=types, socials=socials, num_records=num_records)

    # Output.
    if csv_name and df is not None:
        df.to_csv(csv_name)
    return df


# API to search organizations.
def crunch_api_org(num_records=-1, since_time=None, sort_order=None,
                   name=None, query=None, domain_name=None, locations=None,
                   types=None, csv_name=None):
    df = get_records(1, since_time=since_time, sort_order=sort_order,
                     name=name, locations=locations, domain_name=domain_name,
                     query=query, types=types, num_records=num_records)

    # Output.
    if csv_name and df is not None:
        df.to_csv(csv_name)
    return df
