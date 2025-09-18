"""
Booker Prize Gender Butterfly Chart
===================================

A butterfly chart showing Booker Prize winners by gender and age bin.
Males are displayed on the left side, females on the right side.
Hover over bars to see detailed information including winner names and novel titles.

Created using Vizro-MCP
"""

import pandas as pd
import plotly.graph_objects as go
from vizro import Vizro
from vizro.models import Dashboard, Page, Card
from vizro.models.types import capture


@capture('graph')
def booker_prize_gender_butterfly(data_frame):
    """
    Creates a butterfly chart showing Booker Prize winners by gender and age bin.
    Hover text displays detailed information including winner names and novel titles.
    
    Args:
        data_frame (pd.DataFrame): DataFrame containing Booker Prize data with 
                                  'GENDER', 'AGE BIN', 'WINNER', and 'NOVEL' columns
    
    Returns:
        plotly.graph_objects.Figure: Butterfly chart figure with detailed hover information
    """
    # Filter out rows with missing gender or age bin data
    df_clean = data_frame.dropna(subset=['GENDER', 'AGE BIN'])
    
    # Get all unique age bins and sort them
    all_age_bins = sorted(df_clean['AGE BIN'].unique())
    
    # Create dictionaries to store winners and novels for each gender/age bin combination
    male_data = {}
    female_data = {}
    
    for age_bin in all_age_bins:
        # Get male winners for this age bin
        male_winners = df_clean[(df_clean['AGE BIN'] == age_bin) & (df_clean['GENDER'] == 'M')]
        male_data[age_bin] = {
            'count': len(male_winners),
            'winners': male_winners['WINNER'].tolist() if not male_winners.empty else [],
            'novels': male_winners['NOVEL'].tolist() if not male_winners.empty else []
        }
        
        # Get female winners for this age bin
        female_winners = df_clean[(df_clean['AGE BIN'] == age_bin) & (df_clean['GENDER'] == 'F')]
        female_data[age_bin] = {
            'count': len(female_winners),
            'winners': female_winners['WINNER'].tolist() if not female_winners.empty else [],
            'novels': female_winners['NOVEL'].tolist() if not female_winners.empty else []
        }
    
    # Prepare data for plotting
    male_values = [-male_data[age_bin]['count'] for age_bin in all_age_bins]  # Negative for left side
    female_values = [female_data[age_bin]['count'] for age_bin in all_age_bins]  # Positive for right side
    
    # Create hover text with winner names and novel titles
    male_hover_text = []
    female_hover_text = []
    
    for age_bin in all_age_bins:
        # Male hover text
        male_info = male_data[age_bin]
        if male_info['count'] > 0:
            winner_novel_pairs = [f"• {winner} - '{novel}'" for winner, novel in zip(male_info['winners'], male_info['novels'])]
            male_hover = f"<b>Male Winners (Age Bin {int(age_bin)})</b><br>Count: {male_info['count']}<br><br>" + "<br>".join(winner_novel_pairs)
        else:
            male_hover = f"<b>Male Winners (Age Bin {int(age_bin)})</b><br>Count: 0<br><br>No winners in this age bin"
        male_hover_text.append(male_hover)
        
        # Female hover text
        female_info = female_data[age_bin]
        if female_info['count'] > 0:
            winner_novel_pairs = [f"• {winner} - '{novel}'" for winner, novel in zip(female_info['winners'], female_info['novels'])]
            female_hover = f"<b>Female Winners (Age Bin {int(age_bin)})</b><br>Count: {female_info['count']}<br><br>" + "<br>".join(winner_novel_pairs)
        else:
            female_hover = f"<b>Female Winners (Age Bin {int(age_bin)})</b><br>Count: 0<br><br>No winners in this age bin"
        female_hover_text.append(female_hover)
    
    # Create the figure
    fig = go.Figure()
    
    # Add male bars (left side, negative values)
    fig.add_trace(go.Bar(
        x=male_values,
        y=all_age_bins,
        orientation='h',
        name='Male',
        marker_color='#1f77b4',
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=male_hover_text,
        text=[abs(val) for val in male_values]
    ))
    
    # Add female bars (right side, positive values)
    fig.add_trace(go.Bar(
        x=female_values,
        y=all_age_bins,
        orientation='h',
        name='Female',
        marker_color='#ff0eef',
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=female_hover_text,
        text=[abs(val) for val in female_values]
    ))
    
    # Update layout
    fig.update_layout(
        title='Booker Prize Winners by Gender and Age Bin',
        xaxis_title='Count',
        yaxis_title='Age Bin',
        xaxis=dict(
            tickvals=list(range(-max([abs(v) for v in male_values] + female_values), 
                                max([abs(v) for v in male_values] + female_values) + 1)),
            ticktext=[str(abs(val)) for val in range(-max([abs(v) for v in male_values] + female_values), 
                                                     max([abs(v) for v in male_values] + female_values) + 1)]
        ),
        yaxis=dict(
            type='category',
            categoryorder='array',
            categoryarray=all_age_bins
        ),
        barmode='overlay',
        bargap=0.1,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        )
    )
    
    # Add a vertical line at x=0 to separate male and female sides
    fig.add_vline(x=0, line_width=1, line_color='black', opacity=0.5)
    
    return fig


def load_booker_prize_data():
    """
    Load the Booker Prize dataset from Excel file.
    
    Returns:
        pd.DataFrame: Loaded dataset
    """
    return pd.read_excel("Booker Prize Dataset Final.xlsx")


def create_dashboard():
    """
    Create a Vizro dashboard with the butterfly chart.
    
    Returns:
        Dashboard: Vizro dashboard object
    """
    data = load_booker_prize_data()
    
    dashboard = Dashboard(
        pages=[
            Page(
                title="Booker Prize Gender Analysis",
                components=[
                    Card(
                        text="# Booker Prize Winners by Gender and Age\n\n"
                             "This butterfly chart shows the distribution of Booker Prize winners "
                             "by gender across different age bins. Males are shown on the left (blue), "
                             "females on the right (magenta).",
                        href="/"
                    )
                ]
            )
        ]
    )
    
    return dashboard


if __name__ == "__main__":
    # Example usage
    print("Loading Booker Prize data...")
    df = load_booker_prize_data()
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    print("\nCreating butterfly chart...")
    fig = booker_prize_gender_butterfly(df)
    
    print("Chart created successfully!")
    print("To display the chart, you can use: fig.show()")
    
    # Uncomment the line below to show the chart
    fig.show()
