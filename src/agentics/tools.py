# src/agentics/tools.py

yfinance = {
    "name": "yfinance",
    "description": "Search for yahoo finance information using the yahoo finance API. Use the user's search query to fill the variable $query.",
    "color": "linear-gradient(rgb(152,37,110), rgb(252,187,13))",
    "iconSrc": "",
    "schema": "[{\"id\":0,\"property\":\"query\",\"description\":\" Enter the user's question \",\"type\":\"string\",\"required\":false}]",
    "func": "const fetch = require('node-fetch');\nconst apiKey = 'cece46b7cbmshffcadb4307494f3p1ab487jsnd97acccd8484';\nconst apiHost = 'apidojo-yahoo-finance-v1.p.rapidapi.com';\n\n\nconst encodedQuery = encodeURIComponent($query); // Encode the query to handle spaces and special characters\nconst url = `https://apidojo-yahoo-finance-v1.p.rapidapi.com/auto-complete?q=${encodedQuery}&region=US}`;\n\nconst options = {\n    method: 'GET',\n    headers: {\n        'X-RapidAPI-Key': apiKey,\n        'X-RapidAPI-Host': apiHost\n    }\n};\n\ntry {\n    const response = await fetch(url, options);\n    const result = await response.json(); // Assuming the API returns JSON\n    return JSON.stringify(result); // Convert the response to a string\n} catch (error) {\n    console.error(error);\n    return ''; // Return an empty string in case of an error\n}\n"
    }