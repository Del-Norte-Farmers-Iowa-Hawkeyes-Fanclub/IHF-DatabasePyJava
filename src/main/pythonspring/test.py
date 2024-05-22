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