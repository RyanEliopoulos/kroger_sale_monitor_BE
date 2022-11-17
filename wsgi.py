"""
    Entry point for gunicorn.
"""

import sale_monitor

app = sale_monitor.create_app()
if __name__ == '__main__':
    app.run()
