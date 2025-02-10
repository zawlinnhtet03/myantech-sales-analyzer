import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit UI
st.title("📊 Sales Performance Visualization")

# Display required columns below the title
st.subheader("📌 **Required Columns:**")
st.write("The uploaded file must include the following columns:")
st.write("1. **Item Name**")
st.write("2. **Region**")
st.write("3. **Category**")
st.write("4. **Total (MMK)**")
st.write("5. **Qty**")

# File upload
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read the file
    file_extension = uploaded_file.name.split(".")[-1]
    
    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("📌 **Preview of Data:**")
    st.dataframe(df.head())
    
    if "Total (MMK)" in df.columns:
        df['Total (MMK)'] = df['Total (MMK)'].astype(str).replace('-', '0').astype(float)
    
    df.columns = df.columns.str.strip()

    # Required columns
    required_columns = ["Region", "Item Name", "Category", "Total (MMK)", "Qty"]
    
    missing_cols = [col for col in required_columns if col not in df.columns]

    if missing_cols:
        st.error(f"⚠️ Missing required columns: {', '.join(missing_cols)}")
    else:

        # Ensure required columns exist
        if all(col in df.columns for col in required_columns):
            
            # 📊 Total Sales by Item
            st.subheader("📌 Total Sales by Item")
            sales_by_item = df.groupby("Item Name")["Total (MMK)"].sum().reset_index()
            fig_sales_item = px.bar(
                sales_by_item,
                x="Item Name",
                y="Total (MMK)",
                title="Total Sales by Item",
                labels={"Total (MMK)": "Sales (MMK)", "Item Name": "Product Name"}
            )
            fig_sales_item.update_layout(xaxis_tickangle=90)
            st.plotly_chart(fig_sales_item)

            # 📊 Quantity Sold by Item
            st.subheader("📌 Quantity Sold by Item")
            qty_by_item = df.groupby("Item Name")["Qty"].sum().reset_index()
            fig_qty_item = px.bar(
                qty_by_item,
                x="Item Name",
                y="Qty",
                title="Quantity Sold by Item",
                labels={"Qty": "Quantity Sold", "Item Name": "Product Name"}
            )
            fig_qty_item.update_layout(xaxis_tickangle=90)  # Rotate labels
            st.plotly_chart(fig_qty_item)

            # #          🥧 Sales Distribution by Category
            # st.subheader("📌 Sales Distribution by Category")
            sales_by_category = df.groupby("Category")["Total (MMK)"].sum().reset_index()
            # fig_sales_category = px.pie(
            #     sales_by_category,
            #     names="Category",
            #     values="Total (MMK)",
            #     title="Sales Distribution by Category"
            # )
            # st.plotly_chart(fig_sales_category)

            # 📊 Total Sales by Region
            st.subheader("📌 Sales by Region")
            sales_by_region = df.groupby("Region")["Total (MMK)"].sum().reset_index()
            fig_sales_region = px.bar(
                sales_by_region,
                x="Region",
                y="Total (MMK)",
                title="Sales by Region",
                labels={"Total (MMK)": "Sales (MMK)", "Region": "Region"}
            )
            st.plotly_chart(fig_sales_region)

            # 📊 Top 5 Products by Sales
            st.subheader("📌 Top 5 Products by Sales")
            top_5_products = sales_by_item.sort_values(by="Total (MMK)", ascending=False).reset_index(drop=True).head(5)
            st.write(top_5_products)

            # 📊 Total Revenue vs Quantity Sold Scatter Plot
            st.subheader("📌 Revenue vs Quantity Sold")
            fig_scatter = px.scatter(
                df,
                x="Qty",
                y="Total (MMK)",
                color="Item Name",
                title="Revenue vs Quantity Sold",
                labels={"Qty": "Quantity Sold", "Total (MMK)": "Total Sales (MMK)", "Item Name": "Product Name"}
            )
            st.plotly_chart(fig_scatter)

            # Automated Insights

            # Total Sales
            total_sales = df["Total (MMK)"].sum()
            st.write(f"📈 **Total Sales:** {total_sales:,.0f} MMK")

            # Top-selling Product
            top_selling_product = sales_by_item.loc[sales_by_item["Total (MMK)"].idxmax()]
            st.write(f"📌 **Top-selling Product:** {top_selling_product['Item Name']} with total sales of {top_selling_product['Total (MMK)']:,.0f} MMK")

            # Total Quantity Sold
            total_qty_sold = df["Qty"].sum()
            st.write(f"📊 **Total Quantity Sold:** {total_qty_sold} units")

            # Sales by Region Insights
            max_sales_region = sales_by_region.loc[sales_by_region["Total (MMK)"].idxmax()]
            st.write(f"🌍 **Top Region by Sales:** {max_sales_region['Region']} with total sales of {max_sales_region['Total (MMK)']:,.0f} MMK")

            # Sales by Category Insights
            max_sales_category = sales_by_category.loc[sales_by_category["Total (MMK)"].idxmax()]
            st.write(f"📦 **Top Category by Sales:** {max_sales_category['Category']} with total sales of {max_sales_category['Total (MMK)']:,.0f} MMK")

        else:
            missing_cols = [col for col in required_columns if col not in df.columns]
            st.warning(f"⚠️ Missing required columns: {', '.join(missing_cols)}")
