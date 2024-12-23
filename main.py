import pandas as pd
from sqlalchemy import create_engine
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
import logging
import re

logging.basicConfig(level=logging.ERROR)

app = FastAPI()

engine = create_engine('postgresql://postgres:harry1130@sku.crgka6sy8spi.us-west-1.rds.amazonaws.com:5432/postgres')

@app.get("/search", response_class=HTMLResponse)
async def search_products(
    title: str = Query(default="", alias="Title"),
    mpn: str = Query(default="", alias="MPN"),
    model: str = Query(default="", alias="Model"),
    ItemPrice: str = Query(default="0", alias="ItemPrice") 
):
    if not mpn and title:
        match = re.search(r'\b\d{5,6}\b', title)  
        if match:
            mpn = match.group(0)
    
    try:
        item_price_float = float(re.sub(r'[^\d.]', '', ItemPrice))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ItemPrice format.")

    item_price_str = str(int(item_price_float))
    print(f"MPN: {mpn}, title: {title}, price :{item_price_str}")

    params = {
        'title': title.lower(),
        'mpn': mpn.lower(),
        'model': model.lower(),
        'item_price': item_price_str
    }
    
    if mpn:  
        try:
            query = """
            SELECT *, ABS("Price in Euro New" - %(item_price)s::integer) AS price_diff
            FROM public."SKU"
            WHERE (LOWER("Reference") = %(mpn)s OR LOWER("Reference") LIKE %(mpn_like)s)
            ORDER BY price_diff
            LIMIT 2
            """
            df_sku = pd.read_sql(query, engine, params={
                'mpn': params['mpn'],
                'mpn_like': f"%{params['mpn']}%",
                'item_price': params['item_price']  
            })

            print(df_sku.head())
            print(df_sku.columns)

            if not df_sku.empty:
                html_parts = [
                    "<style>",
                    "body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }",
                    ".card-container { display: flex; justify-content: center; align-items: center;  width: 100%; }",
                    ".card { border: none; border-radius: 12px; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1); background-color: #fff; width: 70%; overflow: hidden; transition: transform 0.3s ease; justify-content: center; align-items: center; margin-left:20%; margin-bottom: 30px; padding: 20px}",
                    ".card:hover { transform: translateY(-10px); }",
                    ".card img { width: 200px; height: auto; }",
                    ".card-content { padding: 20px; }",
                    ".card-table { width: 100%; }",  # New CSS for table layout
                    ".card-title { font-size: 1.5em; margin-bottom: 15px; color: #333; }",
                    ".card-text { color: #666; margin-bottom: 15px; line-height: 1.6; }",
                    ".card-price { font-weight: bold; color: #e63946; font-size: 1.2em; }",
                    "</style>",
                    "<div class='card-container'>"
                ]

                for _, row in df_sku.iterrows():
                    html_parts.append("<div class='card'>")
                    html_parts.append("<div class='card-content'>")
                    html_parts.append(f"<div class='card-title'> {row.get('Name', '')}</div>")
                    html_parts.append("<table class='card-table'><tr>")  # Start table row
                    html_parts.append(f"<td><img src='{row.get('Picture URL', '')}' alt='{row.get('Name', '')}'></td>")  # Picture URL
                    html_parts.append("<td><div class='card-text'>") 
                    html_parts.append(f"Reference: {row.get('Reference', '')}<br>")  # Reference
                    html_parts.append(f"Family: {row.get('Family', '')}<br>")  # Family
                    html_parts.append(f"Brand: {row.get('Brand', '')}<br>")  # Brand
                    html_parts.append(f"Price: {row.get('Price in Euro New', '')}<br>")  # Price
                    html_parts.append(f"Produced: {row.get('Produced', '')}<br>")  # Produced
                    html_parts.append(f"Materials: {row.get('Case | Materials', '')}<br>")
                    html_parts.append(f"Glass: {row.get('Case | Glass', '')}")
                    html_parts.append("</div></td>")  # Close card-text and table cell
                    html_parts.append("</tr></table>")  # Close table row and table
                    html_parts.append(f"<div class='card-text'>Description: {row.get('Description', '')}</div>") # Description
                    html_parts.append("</div></div>")        
                html_parts.append("</div>")
                return ''.join(html_parts)
            else:
                return "No matches found."
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            raise HTTPException(status_code=500, detail="An internal error occurred. Please try again later.")
    else:
        return "No matches found."

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()