"""
Define variables.
"""
import os

# Main path #
ABS_PATH = os.path.abspath(os.path.dirname("__main__"))
HOME_PATH = os.path.join(ABS_PATH + "../../")

# Reference area #
AREA = ['서울', '인천', '동두천', '수원', '원주', '강릉', '대전', '세종', '청주', '서산', '광주', '전주', '순천', '부산', '대구', '울산', '경주시', '창원', '제주']

# Reference class #
WS_LIST = ['A', 'B', 'C', 'D']
WD_LIST = ['ZERO', 'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

# Reference year #
YEAR = [2019, 2020, 2021]
MONTH = [12, 1, 2, 3, 'All']
