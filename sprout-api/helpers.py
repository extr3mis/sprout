import board
import adafruit_mcp3xxx.mcp3008 as MCP

def getPin(pin: int):
    return getattr(board, f'D{pin}')

def getChannel(channel: int):
    return getattr(MCP, f'P{channel}')