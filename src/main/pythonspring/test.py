from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import logging

app = Flask(__name__)


# In-memory database for simplicity
farms = {}
crops = {
    'wheat': {'growth_time': timedelta(minutes=5)},
    'corn': {'growth_time': timedelta(minutes=10)}
}

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/create_farm', methods=['POST'])
def create_farm():
    data = request.json
    farm_id = data.get('farm_id')
    if not farm_id:
        return jsonify({'error': 'Farm ID is required'}), 400
    if farm_id in farms:
        return jsonify({'error': 'Farm already exists'}), 400
    farms[farm_id] = {'crops': [], 'created_at': datetime.now()}
    logger.info(f"Farm {farm_id} created successfully")
    return jsonify({'message': 'Farm created successfully', 'farm_id': farm_id})

@app.route('/plant_crop', methods=['POST'])
def plant_crop():
    data = request.json
    farm_id = data.get('farm_id')
    crop_type = data.get('crop_type')
    if not farm_id or not crop_type:
        return jsonify({'error': 'Farm ID and Crop type are required'}), 400
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
    logger.info(f"Crop {crop_type} planted in farm {farm_id}")
    return jsonify({'message': 'Crop planted successfully', 'crop': crop})

@app.route('/harvest_crop', methods=['POST'])
def harvest_crop():
    data = request.json
    farm_id = data.get('farm_id')
    if not farm_id:
        return jsonify({'error': 'Farm ID is required'}), 400
    if farm_id not in farms:
        return jsonify({'error': 'Farm does not exist'}), 400
    
    harvested_crops = []
    for crop in farms[farm_id]['crops']:
        if datetime.now() >= crop['ready_at']:
            harvested_crops.append(crop)
    
    farms[farm_id]['crops'] = [crop for crop in farms[farm_id]['crops'] if crop not in harvested_crops]
    logger.info(f"Crops harvested from farm {farm_id}")
    return jsonify({'message': 'Crops harvested', 'harvested_crops': harvested_crops})

@app.route('/farm_status', methods=['GET'])
def farm_status():
    farm_id = request.args.get('farm_id')
    if not farm_id:
        return jsonify({'error': 'Farm ID is required'}), 400
    if farm_id not in farms:
        return jsonify({'error': 'Farm does not exist'}), 400
    
    return jsonify(farms[farm_id])

@app.route('/list_farms', methods=['GET'])
def list_farms():
    return jsonify({'farms': list(farms.keys())})

@app.route('/delete_farm', methods=['DELETE'])
def delete_farm():
    data = request.json
    farm_id = data.get('farm_id')
    if not farm_id:
        return jsonify({'error': 'Farm ID is required'}), 400
    if farm_id not in farms:
        return jsonify({'error': 'Farm does not exist'}), 400
    
    del farms[farm_id]
    logger.info(f"Farm {farm_id} deleted")
    return jsonify({'message': 'Farm deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

# Example cURL commands

# Create a farm
# curl -X POST -H "Content-Type: application/json" -d '{"farm_id": "farm1"}' http://127.0.0.1:5000/create_farm

# Plant a crop
# curl -X POST -H "Content-Type: application/json" -d '{"farm_id": "farm1", "crop_type": "wheat"}' http://127.0.0.1:5000/plant_crop

# Harvest crops
# curl -X POST -H "Content-Type: application/json" -d '{"farm_id": "farm1"}' http://127.0.0.1:5000/harvest_crop

# Get farm status
# curl -X GET "http://127.0.0.1:5000/farm_status?farm_id=farm1"

# List all farms
# curl -X GET "http://127.0.0.1:5000/list_farms"

# Delete a farm
# curl -X DELETE -H "Content-Type: application/json" -d '{"farm_id": "farm1"}' http://127.0.0.1:5000/delete_farm

## ROHIN WORK ON THIS PART PLEASE BRO

@app.route('/plant_crop', methods=['POST'])
def plant_crop():
    data = request.json
    farm_id = data.get('farm_id')
    crop_type = data.get('crop_type')
    if not farm_id or not crop_type:
        return jsonify({'error': 'Farm ID and Crop type are required'}), 400
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
    logger.info(f"Crop {crop_type} planted in farm {farm_id}")
    return jsonify({'message': 'Crop planted successfully', 'crop': crop})