from sense_hat import SenseHat
from sense_hat.exceptions import InvalidGainError, InvalidIntegrationCyclesError
from time import sleep, time
import logging 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SECONDS_PER_TEST = 10
sense = SenseHat()

def measure(seconds_per_test: int) -> None:
    stop_time = time() + seconds_per_test
    while time() > stop_time: 
        sleep(2 * sense.colour.integration_time)
        red, green, blue, clear = sense.colour.colour # readings scaled to 0-256
        logger.info(f"R: {red}, G: {green}, B: {blue}, C: {clear}")


logger.info("Testing that readings with default values work...")
try:
    measure(SECONDS_PER_TEST)
except Exception as e:
    logger.error(f"Received {e} while running default test. Quitting...")
    quit()

# A higher gain setting means the
# output will be higher for the same input...
# 
# There are four possible gain values for the colour sensor: 
# 1, 4, 16 and 60, with the default value being 1. 
# You can get or set the sensor gain through the gain property of the ColourSensor object. 
# An attempt to set the gain to a value that is not valid will result in a ValueError exception being raised.

gain = (1,4,16,60)
logger.info("Testing setting the gain...") 
for g in gain:
    sense.color.gain = g
    logger.info(f"Gain: {g}")
    measure(SECONDS_PER_TEST)
    

invalid_gain = (2, 8, 32)
logger.info("Testing setting an invalid gain... expecting a InvalidGainError.")
for g in invalid_gain:
    try:
        sense.color.gain = g
        logger.info(f"Gain: {g}")
        measure(SECONDS_PER_TEST)
    except InvalidGainError as e:
        logger.info(f"Received InvalidGainError {e} as expected!")


sense.color.gain=1 # reset
# Any integer between 1 and 256.
# The default is 1. Each cycle is 2.4ms long.
logger.info("Testing setting the number of integration cycles...")
for num in range(1,257):
    sense.color.integration_cycle = num
    logger.info(f"Integration cycle: {num}")
    measure(SECONDS_PER_TEST)

sense.color.integration_cycle = 2
invalid = (0,257)
logger.info("Testing setting an invalid integration cycle.")
for i in invalid:
    logger.info(f"Integration cycle: {num}")
    try:
        sense.color.integration_cycle = i
        measure(SECONDS_PER_TEST)
    except InvalidIntegrationCyclesError as e:
        logger.info(f"Received {e} as expected")

logger.info("Tests completed")
