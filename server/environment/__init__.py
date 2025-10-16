from pathlib import Path

this_dir = Path(__file__).parent

# Environment accessiblity with varirables
dev = this_dir / 'env/dev.env'
prod = this_dir / 'env/prod.env'