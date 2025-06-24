import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from pandas import DataFrame


def plot_revenue_by_month_year(df: DataFrame, year: int=2017, output_path=None):
    """Plot revenue by month in a given year

    Args:
        df (DataFrame): Dataframe with revenue by month and year query result
        year (int): It could be 2016, 2017 or 2018
        output_path (str, optional): Path to save the plot image. If None, show plot.
    """
    matplotlib.rc_file_defaults()
    sns.set_style(style=None, rc=None)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    sns.lineplot(data=df[f"Year{year}"], marker="o", sort=False, ax=ax1)
    ax2 = ax1.twinx()

    sns.barplot(data=df, x="month", y=f"Year{year}", alpha=0.5, ax=ax2)
    ax1.set_title(f"Revenue by month in {year}")

    if output_path:
        fig.savefig(f"{output_path}/plot_revenue_by_month_year.png")
    else:
        plt.show()


def plot_real_vs_predicted_delivered_time(df: DataFrame, year: int=2017, output_path=None):
    """Plot real vs predicted delivered time by month in a given year

    Args:
        df (DataFrame): Dataframe with real vs predicted delivered time by month and
                        year query result
        year (int): It could be 2016, 2017 or 2018
    """
    matplotlib.rc_file_defaults()
    sns.set_style(style=None, rc=None)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    sns.lineplot(data=df[f"Year{year}_real_time"], marker="o", sort=False, ax=ax1, label="Real time")   
    # sns.lineplot(data=df[f"Year{year}_real_time"], marker="o", sort=False, ax=ax1)
    ax1.twinx()
    g = sns.lineplot(
        data=df[f"Year{year}_estimated_time"], marker="o", sort=False, ax=ax1, label="Estimated time"
    )      
    # g = sns.lineplot(
    #     data=df[f"Year{year}_estimated_time"], marker="s", sort=False, ax=ax1
    # )
    g.set_xticks(range(len(df)))
    g.set_xticklabels(df.month.values)
    g.set(xlabel="month", ylabel="Average days delivery time", title="some title")
    ax1.set_title(f"Average days delivery time by month in {year}")
    ax1.legend()  
    # ax1.legend(["Real time", "Estimated time"])

    if output_path:
        fig.savefig(f"{output_path}/real_vs_predicted_delivered_time.png")
    else:
        plt.show()



# def plot_global_amount_order_status(df: DataFrame):
#     """Plot global amount of order status

#     Args:
#         df (DataFrame): Dataframe with global amount of order status query result
#     """
#     _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

#     elements = [x.split()[-1] for x in df["order_status"]]

#     wedges, autotexts = ax.pie(df["Ammount"], textprops=dict(color="w"))

#     ax.legend(
#         wedges,
#         elements,
#         title="Order Status",
#         loc="center left",
#         bbox_to_anchor=(1, 0, 0.5, 1),
#     )

#     plt.setp(autotexts, size=8, weight="bold")

#     ax.set_title("Order Status Total")

#     my_circle = plt.Circle((0, 0), 0.7, color="white")
#     p = plt.gcf()
#     p.gca().add_artist(my_circle)

#     plt.show()



def plot_global_amount_order_status(df: DataFrame, output_path=None):
    status_summary = df.groupby('order_status')['Ammount'].sum().reset_index()
    status_summary = status_summary.sort_values(by='Ammount', ascending=False)
    status_summary['label'] = status_summary['order_status'].str.replace('order_', '').str.capitalize()
    
    fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(aspect="equal"))

    # --- Outer Ring ---
    # Define a formatter to show percentages only for slices large enough to not clutter the chart.
    def autopct_formatter(pct):
        return f'{pct:.1f}%' if pct > 2 else ''

    # Add the 'autopct' parameter to display percentages on the outer wedges.
    wedges_outer, _, autotexts_outer = ax.pie(
        status_summary['Ammount'],
        colors=plt.cm.Set3(range(len(status_summary))),
        radius=1,
        startangle=90,
        wedgeprops=dict(width=0.3, edgecolor='white', linewidth=2),
        autopct=autopct_formatter,
        pctdistance=0.85, # Position percentages inside the wedges
        textprops={'color':"black", 'weight': 'bold'}
    )
    # Style the outer percentage text for better visibility.
    for autotext in autotexts_outer:
        autotext.set_fontsize(9)

    # --- Inner Ring ---
    delivered_mask = status_summary['order_status'].str.contains('delivered', case=False)
    delivered_total = status_summary[delivered_mask]['Ammount'].sum()
    others_total = status_summary[~delivered_mask]['Ammount'].sum()

    inner_data = [delivered_total, others_total]
    inner_labels = ['Delivered', 'Others']
    
    _, _, autotexts_inner = ax.pie(
        inner_data,
        labels=inner_labels,
        autopct='%1.1f%%',
        colors=['#90EE90', '#FFB6C1'],
        radius=0.7,
        startangle=90,
        wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
        textprops={'fontsize': 12, 'weight': 'bold'}
    )
    for autotext in autotexts_inner:
        autotext.set_color('white')
        autotext.set_weight('bold')

    
    total_amount = status_summary['Ammount'].sum()
    ax.text(0, 0, f'Total\n{total_amount:,.0f}',
            ha='center', va='center', fontsize=16, weight='bold')

    
    legend_labels = [f"{label}: {amount:,.0f}" 
                     for label, amount in zip(status_summary['label'], status_summary['Ammount'])]
    
    ax.legend(wedges_outer, legend_labels,
              title="Status Breakdown (Quantity)",
              loc="center left",
              bbox_to_anchor=(1.05, 0.5),
              fontsize=11)

    ax.set_title("Distribution of Order Quantity by Status",
                 fontsize=18, weight='bold', pad=20)
    
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    if output_path:
        fig.savefig(f"{output_path}/global_amount_order_status.png")
    else:
        plt.show()

def plot_revenue_per_state(df: DataFrame, output_path=None):
    """Plot revenue per state

    Args:
        df (DataFrame): Dataframe with revenue per state query result
    """
    fig = px.treemap(
        df, path=["customer_state"], values="Revenue", width=800, height=400
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    if output_path:
        file_path = f"{output_path}/revenue_per_state.png"
        print(f"Saving plot to {file_path}")
        fig.write_image(file_path)
    else:
        fig.show()


def plot_top_10_least_revenue_categories(df: DataFrame, output_path=None):
    """Plot top 10 least revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 least revenue categories query result
        output_path (str, optional): Path to save the plot image. If None, show plot.
    """
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = df["Category"]

    revenue = df["Revenue"]
    wedges, autotexts = ax.pie(revenue, textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Top 10 Revenue Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    my_circle = plt.Circle((0, 0), 0.7, color="white")
    fig.gca().add_artist(my_circle)

    ax.set_title("Top 10 Least Revenue Categories ammount")

    if output_path:
        fig.savefig(f"{output_path}/top_10_least_revenue_categories.png")
    else:
        plt.show()


def plot_top_10_revenue_categories_ammount(df: DataFrame, output_path=None):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    # Plotting the top 10 revenue categories ammount
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = df["Category"]

    revenue = df["Revenue"]
    wedges, autotexts = ax.pie(revenue, textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Top 10 Revenue Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")
    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    ax.set_title("Top 10 Revenue Categories ammount")

    if output_path:
        fig.savefig(f"{output_path}/top_10_revenue_categories_ammount.png")
    else:
        plt.show()


def plot_top_10_revenue_categories(df: DataFrame, output_path=None):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    fig = px.treemap(df, path=["Category"], values="Num_order", width=800, height=400)
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    if output_path:
        file_path = f"{output_path}/plot_top_10_revenue_categories.png"
        print(f"Saving plot to {file_path}")
        fig.write_image(file_path)
    else:
        fig.show()


def plot_freight_value_weight_relationship(df: DataFrame, output_path=None):
    """Plot freight value weight relationship

    Args:
        df (DataFrame): Dataframe with freight value weight relationship query result
        output_path (str, optional): Path to save the plot image. If None, show plot.
    """
    # TODO: plot freight value weight relationship using seaborn scatterplot.
    # Your x-axis should be weight and, y-axis freight value.
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='product_weight_g', y='freight_value', ax=ax)
    ax.set_title('Freight Value vs Product Weight Relationship')
    ax.set_xlabel('Product Weight (grams)')
    ax.set_ylabel('Freight Value')
    ax.grid(True)
    if output_path:
        fig.savefig(f"{output_path}/freight_value_weight_relationship.png")
    else:
        plt.show()


# def plot_delivery_date_difference(df: DataFrame):
#     """Plot delivery date difference

#     Args:
#         df (DataFrame): Dataframe with delivery date difference query result
#     """
#     plt.figure(figsize=(10, 6))
#     sns.barplot(data=df, x="Delivery_Difference", y="State").set(
#         title="Difference Between Delivery Estimate Date and Delivery Date"
#     )

def plot_delivery_date_difference(df: DataFrame, output_path=None):
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(
        data=df,
        x='Delivery_Difference',
        y='State',
        hue='State',
        palette='viridis',
        dodge=False,
        ax=ax
    )
    ax.set_title(
        'Difference Between Delivery Estimate Date and Delivery Date',
        fontsize=16, weight='bold'
    )
    ax.set_xlabel('Delivery Date Difference (days)', fontsize=12)
    ax.set_ylabel('State', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    if output_path:
        fig.savefig(f"{output_path}/delivery_difference.png")
    else:
        plt.show() 


def plot_order_amount_per_day_with_holidays(df: DataFrame, output_path=None):
    """Plot order amount per day with holidays

    Args:
        df (DataFrame): Dataframe with order amount per day with holidays query result
        output_path (str, optional): Path to save the plot image. If None, show plot.
    """
    # TODO: plot order amount per day with holidays using matplotlib.
    # Mark holidays with vertical lines.
    # Hint: use plt.axvline.
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot order count timeline
    ax.plot(df['date'], df['order_count'], 
             marker=',', linestyle='-', label='Daily Orders')
    
    # Add holiday markers
    holiday_rows = df[df['holiday'] == True]
    for idx, row in holiday_rows.iterrows():
        ax.axvline(x=row['date'], color='red', linestyle='--', 
            alpha=0.7, label='Holiday' if idx == holiday_rows.index[0] else "")
    
    # Formatting
    ax.set_title('Daily Order Count with Holiday Indicators')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Orders')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    ax.legend()  
    plt.tight_layout()
    if output_path:
        fig.savefig(f"{output_path}/order_amount_per_day_with_holidays.png")
    else:
        plt.show()
