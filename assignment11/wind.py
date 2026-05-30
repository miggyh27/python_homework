import plotly.express as px
import plotly.data as pldata

df = pldata.wind(return_type="pandas")

print("First 10 rows:")
print(df.head(10))
print("\nLast 10 rows:")
print(df.tail(10))


df["strength"] = df["strength"].str.replace(r"[-+].*", "", regex=True).astype(float)

print("\nstrength dtype after cleaning:", df["strength"].dtype)

fig = px.scatter(
    df,
    x="strength",
    y="frequency",
    color="direction",
    title="Wind Strength vs. Frequency by Direction",
)

fig.write_html("wind.html")


with open("wind.html", encoding="utf-8") as f:
    html = f.read()

assert "plotly" in html.lower(), "wind.html does not look like a Plotly plot"
print(f"\nwind.html written and verified ({len(html)} chars).")
