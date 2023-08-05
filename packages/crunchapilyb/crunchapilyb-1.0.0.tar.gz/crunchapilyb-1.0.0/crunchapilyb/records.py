import pandas as pd
from threading import Thread
from .trigger import trigger_api

# A global variable: a DataFrame to record results.
df_records = []


def get_records(ppl_or_org, since_time=None, sort_order=None,
                num_records=-1, name=None, query=None, domain_name=None,
                locations=None, types=None, socials=None):
    global df_records

    # Trigger API to get basic info.
    api_response = trigger_api(ppl_or_org, since_time=since_time,
                               sort_order=sort_order, name=name, query=query,
                               domain_name=domain_name, locations=locations,
                               types=types, socials=socials)
    ''''data': {'paging': {'total_items': 2237,
                            'number_of_pages': 23,
                            'current_page': 1,
                            'sort_order': 'updated_at ASC',
                            'items_per_page': 100,
                            'next_page_url': ...,
                            'prev_page_url': None,
                            'key_set_url': '...,
                            'collection_url': ...,
                            'updated_since': '1597017600'},
                 'items': [{'type': 'OrganizationSummary',
                            'uuid': ...,
                            'properties': {'permalink': '...',... }
                            },...]
                }'''

    # Adjust the number of records.
    total_items = api_response['data']['paging']['total_items']
    # When no element is found, return None.
    if not total_items:
        print("No item found")
        return None
    # If num_records <= 0 or too large, set it as total items found.
    if num_records <= 0 or num_records > total_items:
        num_records = total_items
    print(num_records, "items found")

    # DataFrame of records.
    df_records = pd.DataFrame(
        columns=api_response['data']['items'][0]['properties'].keys())

    # Calculate total number of pages to iterate.
    items_per_page = api_response['data']['paging']['items_per_page']
    page_num = (num_records // items_per_page)
    if num_records % 100:
        page_num += 1
    print(page_num, "pages in total")

    thread_group = []

    # Iterate through pages using multithreading.
    def iterate_through_pages(i):
        global df_records
        print("Operating thread of page", i)

        # Visit page i.
        api_response_ = trigger_api(ppl_or_org, page=i, since_time=since_time,
                                    sort_order=sort_order, name=name,
                                    query=query, domain_name=domain_name,
                                    locations=locations, types=types,
                                    socials=socials)

        # Add records to Dataframe df_temp.
        idx_ = (i - 1) * items_per_page + 1
        df_temp = pd.DataFrame(
            columns=api_response['data']['items'][0]['properties'].keys())
        for item in api_response_["data"]["items"]:
            df_temp = df_temp.append(pd.Series(item['properties'], name=idx_))
            idx_ += 1

        # Append df_temp to df_records.
        df_records = df_records.append(df_temp)

    # Create a thread group.
    for page in range(1, page_num):
        # Trigger API
        page_thread = Thread(target=iterate_through_pages, args=(page,))
        thread_group.append(page_thread)
        page_thread.start()

    # Join all threads.
    for page_thread in thread_group:
        page_thread.join()

    # Sort df_records by index.
    df_records.sort_index(inplace=True)

    # Process the last page.
    api_response = trigger_api(ppl_or_org, page=page_num, query=query,
                               since_time=since_time, sort_order=sort_order,
                               domain_name=domain_name, locations=locations,
                               name=name, types=types, socials=socials)
    idx = (page_num - 1) * items_per_page + 1
    for itm in api_response["data"]["items"][
                :num_records - (page_num - 1) * items_per_page]:
        df_records = df_records.append(pd.Series(itm['properties'], name=idx))
        idx += 1

    return df_records
