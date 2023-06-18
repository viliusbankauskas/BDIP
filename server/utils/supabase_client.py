from supabase import create_client

SUPABASE_URL="https://rhsviqitxauosudiuaew.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJoc3ZpcWl0eGF1b3N1ZGl1YWV3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODU3OTU4MjgsImV4cCI6MjAwMTM3MTgyOH0.E-HB9Io5yL_f24uGWl0meRmtvlzv5Se6BaJfo1ZGy8g"
TABLE = "big_data"

def db_client():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except:
        print("An exception occurred: create_client")

def select_entry(id, table=TABLE):
    print("Checking for: ", id)
    db = db_client()
    data = dict()
    try:
        entry = db.table(table).select("*").eq("wikidata_id", id).execute()
        response = entry.data[0]

        if response:
            similar_text_items = get_similar([response['sim_text_one'], response['sim_text_two'], response['sim_text_three']])
            similar_location_items = get_similar([response['first_closest'], response['second_closest'],response['third_closest']])
            similar_color_items = db.table(table).select("*").eq("color_cluster", response['color_cluster']).neq("wikidata_id", id).limit(3).execute().data

            data = {
                'entry': response,
                'similar_by_text': similar_text_items,
                'similar_by_location': similar_location_items,
                'similar_by_color': similar_color_items
            }
        
    except Exception as e:
        print(f"An exception occurred: {e}")

    return data

def get_similar(values, table=TABLE):
    db = db_client()
    similar_items = []
    try:
        for id in values:
            item = db.table(table).select("*").eq("wikidata_id", id).execute()
            if item:
                similar_items.append(item.data[0])
    except:
        print("An exception occurred: get_similar")

    return similar_items

def all_entries(table=TABLE):
    print("Fetch entries...")

    db = db_client()
    data = []
    try:
        entries = db.table(table).select("*").execute()
        data = entries.data
    except:
        print("An exception occurred: all_entries")

    return data

def update_entry(entry_id, table=TABLE, **kwargs):
    db = db_client()
    try:
        entry = db.table(table).update(kwargs).eq("wikidata_id", entry_id).execute()
        return entry
    except Exception as e:
        print(f"An exception occurred: {e}")

