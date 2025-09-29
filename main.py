import os
import sys
from pathlib import Path
from tg_bot.bot import main

current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from tg_bot.bot import main

if __name__ == "__main__":
    main()