from techcrunch import extract_articles
from save import save_to_file

trend_report=extract_articles()
save_to_file(trend_report)

