from flask import Flask, request, jsonify, json
from flask_cors import CORS

from utils.supabase_client import select_entry, update_entry, all_entries
from utils.scrape import get_title_imglink
from utils.calculate_nearest import nearest_text, nearest_locations, nearest_color_cluster

app = Flask(__name__)
CORS(app)

@app.route("/entry", methods=["POST"])
def entry():
    data = request.get_json()
    
    if data is None:
        return jsonify({"error": "Invalid JSON data"}), 400

    title, lat, lon, description, local_image_path = get_title_imglink(data['wikidata_id'])

    updated = update_entry_data(data['wikidata_id'], data, title, lat, lon, description, local_image_path)

    return jsonify(updated)

@app.route("/")
def all():
    entries = all_entries()

    return jsonify(entries)

def update_entry_data(entry_id, entry, title, lat, lon, description, local_image_path):
    current_entry = entry
    all_data = None


    update_data = {}
    if current_entry.get('name') != title and title is not None:
        update_data['name'] = title

    if current_entry.get('latitude') != lat and lat is not None:
        update_data['latitude'] = lat

    if current_entry.get('longitude') != lon and lon is not None:
        update_data['longitude'] = lon

    if current_entry.get('image_link') != local_image_path and local_image_path is not None:
        update_data['image_link'] = local_image_path

    if current_entry.get('description') != description and description is not None:
        update_data['description'] = description

        all_data = all_entries()
        
        sim_text_one, sim_text_two, sim_text_three = nearest_text(all_data, description)
        update_data['sim_text_one'] = sim_text_one
        update_data['sim_text_two'] = sim_text_two
        update_data['sim_text_three'] = sim_text_three

    if 'latitude' in update_data or 'longitude' in update_data:
        if all_data is None:
            all_data = all_entries()

        first_closest, second_closest, third_closest = nearest_locations(all_data, lat, lon)
        update_data['first_closest'] = first_closest
        update_data['second_closest'] = second_closest
        update_data['third_closest'] = third_closest

    if 'image_link' in update_data:
        if all_data is None:
            all_data = all_entries()
            
        update_data['color_cluster'] = nearest_color_cluster(all_data, entry_id)

    if update_data:
        update_entry(entry_id, **update_data)

    return select_entry(entry_id)
