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
                    "<!DOCTYPE html>",
                    "<html lang='en'>",
                    "<head>",
                    "    <meta charset='UTF-8'>",
                    "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
                    "    <title>Watch Information</title>",
                    "    <link href='https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap' rel='stylesheet'>",
                    "    <style>",
                    "        body { font-family: 'Roboto', sans-serif; margin: 20px; background: linear-gradient(to right, #d9a7c7 0%, #fffcdc 100%); min-width: 1043px; }",
                    "        h1 { text-align: center; color: #333; margin-bottom: 20px; font-size: 25px; }",
                    "        .container { display: flex; justify-content: center; flex-direction: row; font-size: 12px; flex-wrap: wrap; }",
                    "        .row { display: flex; flex-direction: column; max-width: 500px; }",
                    "        .basic-info, .movement, .case, .dial, .view-pictures { flex: 1; padding: 20px; background-color: #fff; transition: transform 0.2s; }",
                    "        .basic-info:hover, .movement:hover, .case:hover, .dial:hover, .view-pictures:hover { transform: scale(1.02); }",
                    "        h2 { color: #007BFF; margin-bottom: 15px; font-size: 20px; }",
                    "        table { width: 100%; border-collapse: collapse; margin-top: 10px; }",
                    "        th, td { border: 1px solid #ccc; padding: 12px; text-align: left; }",
                    "        th { background-color: #007BFF; color: white; }",
                    "        tr:nth-child(even) { background-color: #f2f2f2; }",
                    "        tr:hover { background-color: #e0e0e0; transition: background-color 0.3s; }",
                    "        .case_style { display: flex; flex-wrap: wrap; gap: 15px; }",
                    "        .button { display: inline-block; padding: 10px 20px; margin-top: 10px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px; transition: background-color 0.3s; }",
                    "        .button:hover { background-color: #0056b3; }",
                    "    </style>",
                    "</head>",
                    "<body>"
                ]

                for _, row in df_sku.iterrows():
                    html_parts.append("    <div class='card'>")
                    html_parts.append(f"        <h1>{row.get('Name', '')}</h1>")
                    html_parts.append("        <div class='container'>")
                    html_parts.append("            <div class='row'>")
                    html_parts.append("                <div class='basic-info'>")
                    html_parts.append("                    <h2>Basic Info</h2>")
                    html_parts.append(f"                    <div>Brand : {row.get('Brand', '')}</div>")
                    html_parts.append(f"                    <div>Family : {row.get('Family', '')}</div>")
                    html_parts.append(f"                    <div>Reference : {row.get('Reference', '')}</div>")
                    html_parts.append(f"                    <div>Produced : {row.get('Produced', '')}</div>")
                    html_parts.append(f"                    <div>Price : {row.get('Price in Euro New', '')}</div>")
                    html_parts.append("                </div>")
                    html_parts.append("                <div class='movement'>")
                    html_parts.append("                    <h2>Movement</h2>")
                    html_parts.append(f"                    <div class='card-text'>{row.get('Movement', 'N/A')}</div>")
                    html_parts.append(f"                    <div class='card-text'>{row.get('Movement 2', 'N/A')}</div>")
                    html_parts.append("                </div>")
                    html_parts.append("            </div>")
                    html_parts.append("            <div class='row'>")
                    html_parts.append("                <div class='case'>")
                    html_parts.append("                    <h2>Case</h2>")
                    html_parts.append("                    <div class='case_style' style='display: flex; flex-wrap: wrap; gap: 10px;'>")
                    html_parts.append(f"                        <div style='flex: 1 1 calc(40% - 10px);'>Materials : {row.get('Case | Materials', 'N/A')}</div>")
                    html_parts.append(f"                        <div style='flex: 1 1 calc(30% - 10px);'>Bezel : {row.get('Case | Bezel', 'N/A')}</div>")
                    html_parts.append(f"                        <div style='flex: 1 1 calc(30% - 10px);'>Glass : {row.get('Case | Glass', 'N/A')}</div>")
                    html_parts.append(f"                        <div style='flex: 1 1 calc(40% - 10px);'>Back : {row.get('Case | Back', 'N/A')}</div>")
                    html_parts.append(f"                        <div style='flex: 1 1 calc(30% - 10px);'>Shape : {row.get('Case | Shape', 'N/A')}</div>")
                    html_parts.append(f"                        <div style='flex: 1 1 calc(30% - 10px);'>Diameter : {row.get('Case | Diameter', 'N/A')}</div>")
                    html_parts.append(f"                        <div style='flex: 1 1 calc(40% - 10px);'>Lug Width : {row.get('Case | Lug Width', 'N/A')}</div>")
                    html_parts.append(f"                        <div style='flex: 1 1 calc(30% - 10px);'>W/R : {row.get('Case | W/R', 'N/A')}</div>")
                    html_parts.append(f"                        <div style='flex: 1 1 calc(30% - 10px);'>Height : {row.get('Case | Height', 'N/A')}</div>")
                    html_parts.append("                    </div>")
                    html_parts.append("                </div>")
                    html_parts.append("                <div class='dial'>")
                    html_parts.append("                    <h2>Dial</h2>")
                    html_parts.append("                    <table>")
                    html_parts.append("                        <tr>")
                    html_parts.append("                            <th>Nickname</th>")
                    html_parts.append("                            <th>Color</th>")
                    html_parts.append("                            <th>Finish</th>")
                    html_parts.append("                            <th>Indexes</th>")
                    html_parts.append("                            <th>Hands</th>")
                    html_parts.append("                        </tr>")
                    html_parts.append("                        <tr>")
                    html_parts.append(f"                            <td>{row.get('Dial | Nickname', 'N/A')}</td>")
                    html_parts.append(f"                            <td>{row.get('Dial | Color', 'N/A')}</td>")
                    html_parts.append(f"                            <td>{row.get('Dial | Finish', 'N/A')}</td>")
                    html_parts.append(f"                            <td>{row.get('Dial | Indexes', 'N/A')}</td>")
                    html_parts.append(f"                            <td>{row.get('Dial | Hands', 'N/A')}</td>")
                    html_parts.append("                        </tr>")
                    html_parts.append("                    </table>")
                    html_parts.append("                </div>")
                    html_parts.append("            </div>")
                    html_parts.append("            <div class='row'>")
                    html_parts.append("                <div class='view-pictures'>")
                    html_parts.append("                    <h2>View Picture</h2>")
                    html_parts.append(f"                    <a href={row.get('Picture URL', '#')} class='button'>View Picture</a>")
                    html_parts.append("                    <h2>View On Google</h2>")
                    html_parts.append(f"                    <a href={row.get('Page Source', '#')} class='button'>View On Google</a>")
                    html_parts.append("                </div>")
                    html_parts.append("            </div>")
                    html_parts.append("        </div>")
                    html_parts.append("    </div>")

                html_parts.append("</body>")
                html_parts.append("</html>")
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