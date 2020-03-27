curl -X POST localhost:5000/api/v1.0/predictions \
    -H 'Content-Type: application/json' \
    -d '{ "data": {"type": "url", "input": "https://raw.githubusercontent.com/jackklpan/seldon_example/master/first_image.jpg"} }'
