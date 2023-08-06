# How to read bag files

Temporary python API for reading bag files. For more details about the API, see the [documentation](https://github.com/biospine/reading_rosbag/blob/master/documentation.md).

# Install

```bash
pip3 install rosbag2-api
```

## Requirements

- sqlite3 (`sudo apt-get install sqlite3`)
- rclpy

# Checkout this development version

```bash
git clone https://github.com/biospine/reading_rosbag.git
```

## Test

```bash
python3 testing_reading_rosbag.py
```

### Input

The `testing_reading_rosbag.py` script opens the [bag file](https://github.com/biospine/reading_rosbag/blob/master/rosbag2_2020_07_13-18_13_16/rosbag2_2020_07_13-18_13_16_0.db3) and reads data.

### Expected output

The `testing_reading_rosbag.py` script saves a .csv file with the same name of the bag file.