from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory database for simplicity
farms = {}
crops = {
    'wheat': {'growth_time': timedelta(minutes=5)},
    'corn': {'growth_time': timedelta(minutes=10)}
}

@app.route('/create_farm', methods=['POST'])
def create_farm():
    data = request.json
    farm_id = data.get('farm_id')
    if farm_id in farms:
        return jsonify({'error': 'Farm already exists'}), 400
    farms[farm_id] = {'crops': [], 'created_at': datetime.now()}
    return jsonify({'message': 'Farm created successfully', 'farm_id': farm_id})

@app.route('/plant_crop', methods=['POST'])
def plant_crop():
    data = request.json
    farm_id = data.get('farm_id')
    crop_type = data.get('crop_type')
    if farm_id not in farms:
        return jsonify({'error': 'Farm does not exist'}), 400
    if crop_type not in crops:
        return jsonify({'error': 'Invalid crop type'}), 400
    
    crop = {
        'type': crop_type,
        'planted_at': datetime.now(),
        'ready_at': datetime.now() + crops[crop_type]['growth_time']
    }
    farms[farm_id]['crops'].append(crop)
    return jsonify({'message': 'Crop planted successfully', 'crop': crop})

@app.route('/harvest_crop', methods=['POST'])
def harvest_crop():
    data = request.json
    farm_id = data.get('farm_id')
    if farm_id not in farms:
        return jsonify({'error': 'Farm does not exist'}), 400
    
    harvested_crops = []
    for crop in farms[farm_id]['crops']:
        if datetime.now() >= crop['ready_at']:
            harvested_crops.append(crop)
    
    farms[farm_id]['crops'] = [crop for crop in farms[farm_id]['crops'] if crop not in harvested_crops]
    
    return jsonify({'message': 'Crops harvested', 'harvested_crops': harvested_crops})

@app.route('/farm_status', methods=['GET'])
def farm_status():
    farm_id = request.args.get('farm_id')
    if farm_id not in farms:
        return jsonify({'error': 'Farm does not exist'}), 400
    
    return jsonify(farms[farm_id])

if __name__ == '__main__':
    app.run(debug=True)

