from pathlib import Path
import random

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Netflix Analytics Studio | Ummi Habiba",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# COLORS
# =========================================================

BACKGROUND = "#0C0A0D"
PANEL = "#171319"
CORAL = "#FF7A6B"
GOLD = "#F3C969"
PURPLE = "#D98DF0"
GREEN = "#8ED1B2"
TEXT = "#F8F4EF"
MUTED = "#B9ADB8"
BORDER = "#3A2B37"

CHART_COLORS = [
    CORAL,
    GOLD,
    PURPLE,
    GREEN,
    "#FFB36B",
    "#C9A7FF"
]

PLOT_CONFIG = {
    "displaylogo": False,
    "responsive": True,
    "scrollZoom": False
}


# =========================================================
# CUSTOM WEBSITE DESIGN
# =========================================================

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(
                    circle at 90% 5%,
                    rgba(255, 122, 107, 0.14),
                    transparent 28rem
                ),
                radial-gradient(
                    circle at 5% 65%,
                    rgba(243, 201, 105, 0.07),
                    transparent 28rem
                ),
                #0C0A0D;
            color: #F8F4EF;
        }

        .block-container {
            max-width: 1280px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    #171319 0%,
                    #100D12 100%
                );
            border-right: 1px solid #3A2B37;
        }

        h1, h2, h3 {
            color: #F8F4EF;
        }

        .netflix-hero {
            position: relative;
            overflow: hidden;
            padding: clamp(2.5rem, 7vw, 5.5rem);
            margin-bottom: 2rem;
            border: 1px solid #3A2B37;
            border-radius: 32px;
            background:
                linear-gradient(
                    135deg,
                    rgba(255, 122, 107, 0.16),
                    rgba(243, 201, 105, 0.04)
                ),
                #171319;
            box-shadow:
                0 30px 90px rgba(0, 0, 0, 0.35);
        }

        .netflix-hero::before {
            content: "";
            position: absolute;
            width: 300px;
            height: 300px;
            top: -130px;
            right: -90px;
            border-radius: 50%;
            background: rgba(255, 122, 107, 0.13);
            box-shadow:
                0 0 0 35px rgba(255, 122, 107, 0.035),
                0 0 0 70px rgba(255, 122, 107, 0.018);
            animation: heroFloat 7s ease-in-out infinite;
        }

        .hero-label {
            position: relative;
            z-index: 2;
            margin-bottom: 1rem;
            color: #F3C969;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.22rem;
            text-transform: uppercase;
        }

        .hero-title {
            position: relative;
            z-index: 2;
            max-width: 900px;
            margin: 0 0 1.25rem;
            color: #F8F4EF;
            font-size: clamp(2.9rem, 7vw, 5.8rem);
            line-height: 0.98;
            letter-spacing: -0.22rem;
        }

        .hero-title span {
            background:
                linear-gradient(
                    120deg,
                    #FF7A6B,
                    #F3C969
                );
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .hero-description {
            position: relative;
            z-index: 2;
            max-width: 760px;
            margin: 0;
            color: #B9ADB8;
            font-size: 1.04rem;
            line-height: 1.8;
        }

        .hero-tags {
            position: relative;
            z-index: 2;
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            margin-top: 1.8rem;
        }

        .hero-tag {
            padding: 0.48rem 0.9rem;
            border: 1px solid #4A3947;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.04);
            color: #DED4DC;
            font-size: 0.76rem;
        }

        .project-notice {
            padding: 1.1rem 1.35rem;
            margin: 1.2rem 0 1.8rem;
            border-left: 4px solid #FF7A6B;
            border-radius: 0 16px 16px 0;
            background: rgba(255, 122, 107, 0.065);
            color: #CFC4CC;
            line-height: 1.7;
        }

        .project-notice strong {
            color: #F3C969;
        }

        [data-testid="stMetric"] {
            padding: 1.25rem;
            border: 1px solid #3A2B37;
            border-radius: 19px;
            background:
                linear-gradient(
                    145deg,
                    rgba(255, 255, 255, 0.045),
                    rgba(255, 255, 255, 0.012)
                );
            transition:
                transform 180ms ease,
                border-color 180ms ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            border-color: #FF7A6B;
        }

        [data-testid="stMetricValue"] {
            color: #FF7A6B;
        }

        [data-testid="stMetricDelta"] {
            color: #F3C969;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: #3A2B37 !important;
            border-radius: 19px !important;
            background: rgba(255, 255, 255, 0.025);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.55rem;
            flex-wrap: wrap;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.75rem 1.1rem;
            border-radius: 999px;
        }

        div[data-testid="stDataFrame"] {
            overflow: hidden;
            border: 1px solid #3A2B37;
            border-radius: 18px;
        }

        .stButton button,
        .stDownloadButton button {
            min-height: 46px;
            border-radius: 12px;
            font-weight: 700;
        }

        .project-footer {
            margin-top: 4rem;
            padding: 1.6rem 0;
            border-top: 1px solid #3A2B37;
            color: #8E828D;
            font-size: 0.8rem;
            line-height: 1.7;
            text-align: center;
        }

        @keyframes heroFloat {
            0%, 100% {
                transform: translateY(0) rotate(0deg);
            }

            50% {
                transform: translateY(20px) rotate(12deg);
            }
        }

        @media (prefers-reduced-motion: reduce) {
            .netflix-hero::before {
                animation: none;
            }

            [data-testid="stMetric"] {
                transition: none;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATASET LOCATION
# =========================================================

DATA_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "netflix_titles.csv"
)


# =========================================================
# DATA FUNCTIONS
# =========================================================

@st.cache_data(show_spinner=False)
def load_data(file_path):
    try:
        dataframe = pd.read_csv(
            file_path,
            encoding="utf-8-sig"
        )

        encoding_used = "UTF-8-SIG"

    except UnicodeDecodeError:
        dataframe = pd.read_csv(
            file_path,
            encoding="cp1252"
        )

        encoding_used = "Windows-1252"

    dataframe.columns = (
        dataframe.columns
        .astype(str)
        .str.strip()
        .str.lower()
    )

    for column in dataframe.columns:
        if (
            pd.api.types.is_object_dtype(dataframe[column])
            or pd.api.types.is_string_dtype(dataframe[column])
        ):
            dataframe[column] = (
                dataframe[column]
                .astype("string")
                .str.strip()
                .replace("", pd.NA)
            )

    if "release_year" in dataframe.columns:
        dataframe["release_year"] = (
            pd.to_numeric(
                dataframe["release_year"],
                errors="coerce"
            )
            .astype("Int64")
        )

        dataframe["_decade"] = (
            dataframe["release_year"] // 10 * 10
        ).astype("Int64")

    if "date_added" in dataframe.columns:
        dataframe["_date_added"] = pd.to_datetime(
            dataframe["date_added"],
            errors="coerce"
        )

    if "duration" in dataframe.columns:
        duration_text = dataframe["duration"].astype("string")

        dataframe["_duration_value"] = (
            pd.to_numeric(
                duration_text.str.extract(r"(\d+)")[0],
                errors="coerce"
            )
            .astype("Int64")
        )

        dataframe["_duration_unit"] = (
            duration_text
            .str.extract(r"\d+\s*(.*)", expand=False)
            .str.strip()
        )

    return dataframe, encoding_used


def split_values(value):
    if pd.isna(value):
        return []

    return [
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    ]


def split_and_count(series):
    if series is None or series.empty:
        return pd.Series(dtype="int64")

    values = (
        series
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    values = values[values != ""]

    return values.value_counts()


def readable(value, fallback="Not provided"):
    if value is None:
        return fallback

    try:
        if pd.isna(value):
            return fallback
    except (TypeError, ValueError):
        pass

    text = str(value).strip()

    return text if text else fallback


def contains_country(value, selected_country):
    return selected_country in split_values(value)


def create_recommendations(
    dataframe,
    selected_title,
    limit=6
):
    """
    Generate transparent, rule-based title recommendations.

    Missing values are checked before comparisons.
    This is not Netflix's real recommendation algorithm.
    """

    selected_rows = dataframe[
        dataframe["title"]
        .fillna("")
        .astype(str)
        .eq(str(selected_title))
    ]

    if selected_rows.empty:
        return pd.DataFrame()

    selected = selected_rows.iloc[0]

    selected_genres = set(
        split_values(selected.get("listed_in"))
    )

    selected_type = selected.get("type", pd.NA)
    selected_rating = selected.get("rating", pd.NA)
    selected_year = selected.get("release_year", pd.NA)

    candidates = dataframe[
        dataframe["title"]
        .fillna("")
        .astype(str)
        .ne(str(selected_title))
    ].copy()

    def calculate_score(row):
        score = 0

        candidate_genres = set(
            split_values(row.get("listed_in"))
        )

        candidate_type = row.get("type", pd.NA)
        candidate_rating = row.get("rating", pd.NA)
        candidate_year = row.get("release_year", pd.NA)

        # Four points for every shared genre.
        shared_genres = selected_genres.intersection(
            candidate_genres
        )

        score += len(shared_genres) * 4

        # Two points for the same content type.
        if (
            pd.notna(selected_type)
            and pd.notna(candidate_type)
            and str(candidate_type) == str(selected_type)
        ):
            score += 2

        # One point for the same rating.
        if (
            pd.notna(selected_rating)
            and pd.notna(candidate_rating)
            and str(candidate_rating) == str(selected_rating)
        ):
            score += 1

        # Points for nearby release years.
        if (
            pd.notna(selected_year)
            and pd.notna(candidate_year)
        ):
            year_difference = abs(
                int(selected_year)
                - int(candidate_year)
            )

            if year_difference <= 3:
                score += 2

            elif year_difference <= 10:
                score += 1

        return score

    candidates["_recommendation_score"] = candidates.apply(
        calculate_score,
        axis=1
    )

    candidates = candidates[
        candidates["_recommendation_score"] > 0
    ]

    candidates = candidates.sort_values(
        by=[
            "_recommendation_score",
            "release_year",
            "title"
        ],
        ascending=[
            False,
            False,
            True
        ],
        na_position="last"
    )

    candidates = candidates.drop_duplicates(
        subset=["title"]
    )

    return candidates.head(limit)

def style_chart(figure, height=420):
    figure.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "color": TEXT,
            "family": "Arial, sans-serif"
        },
        margin={
            "l": 25,
            "r": 25,
            "t": 45,
            "b": 30
        },
        hoverlabel={
            "bgcolor": PANEL,
            "font_color": TEXT,
            "bordercolor": BORDER
        }
    )

    figure.update_xaxes(
        gridcolor="rgba(255,255,255,0.07)"
    )

    figure.update_yaxes(
        gridcolor="rgba(255,255,255,0.07)"
    )

    return figure


# =========================================================
# LOAD DATA
# =========================================================

if not DATA_FILE.exists():
    st.error("The project dataset could not be found.")

    st.write(
        "Create a `data` folder beside `app.py` and place "
        "`netflix_titles.csv` inside it."
    )

    st.code(str(DATA_FILE))
    st.stop()


try:
    df, encoding_used = load_data(DATA_FILE)

except pd.errors.EmptyDataError:
    st.error("The Netflix CSV file is empty.")
    st.stop()

except pd.errors.ParserError as error:
    st.error("The CSV structure could not be read.")
    st.code(str(error))
    st.stop()

except Exception as error:
    st.error("The dataset could not be loaded.")
    st.code(str(error))
    st.stop()


required_columns = {
    "title",
    "type",
    "release_year"
}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    st.error(
        "Missing required columns: "
        + ", ".join(sorted(missing_columns))
    )

    st.write("Columns found:", df.columns.tolist())
    st.stop()


source_columns = [
    column
    for column in df.columns
    if not column.startswith("_")
]


# =========================================================
# HERO
# =========================================================

# =========================================================
# HERO
# =========================================================

st.html(
    """
<section class="netflix-hero">
    <div class="hero-label">
        Completed Interactive Analytics Project
    </div>

    <h1 class="hero-title">
        Netflix Analytics
        <span>Studio.</span>
    </h1>

    <p class="hero-description">
        Explore more than 8,000 catalog records, examine
        content trends, investigate genres and countries,
        review data quality, and discover related titles
        through a transparent recommendation system.
    </p>

    <div class="hero-tags">
        <span class="hero-tag">Python</span>
        <span class="hero-tag">Pandas</span>
        <span class="hero-tag">Plotly</span>
        <span class="hero-tag">Streamlit</span>
        <span class="hero-tag">Interactive analytics</span>
    </div>
</section>
    """
)

st.caption(
    "Independent portfolio project by Ummi Habiba. "
    "Not affiliated with or endorsed by Netflix."
)

st.caption(
    "Independent portfolio project by Ummi Habiba. "
    "Not affiliated with or endorsed by Netflix."
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

available_types = sorted(
    df["type"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

valid_years = (
    df["release_year"]
    .dropna()
    .astype(int)
)

minimum_year = int(valid_years.min())
maximum_year = int(valid_years.max())

country_options = (
    split_and_count(df["country"])
    .index
    .astype(str)
    .tolist()
    if "country" in df.columns
    else []
)

rating_options = (
    sorted(
        df["rating"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    if "rating" in df.columns
    else []
)


with st.sidebar:
    st.title("🎬 Netflix Studio")

    st.caption(
        "Completed analytics project by Ummi Habiba"
    )

    st.success(
        f"{len(df):,} records loaded automatically."
    )

    st.caption(f"Encoding: {encoding_used}")

    st.divider()

    st.subheader("Explore the catalog")

    title_search = st.text_input(
        "Search by title",
        placeholder="Example: Stranger Things"
    )

    selected_types = st.multiselect(
        "Content type",
        options=available_types,
        default=available_types
    )

    selected_years = st.slider(
        "Release-year range",
        min_value=minimum_year,
        max_value=maximum_year,
        value=(minimum_year, maximum_year)
    )

    selected_country = st.selectbox(
        "Country",
        options=["All countries"] + country_options
    )

    selected_ratings = st.multiselect(
        "Rating labels",
        options=rating_options
    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if title_search:
    filtered_df = filtered_df[
        filtered_df["title"]
        .fillna("")
        .astype(str)
        .str.contains(
            title_search,
            case=False,
            regex=False,
            na=False
        )
    ]

if selected_types:
    filtered_df = filtered_df[
        filtered_df["type"].isin(selected_types)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

filtered_df = filtered_df[
    filtered_df["release_year"].between(
        selected_years[0],
        selected_years[1]
    )
]

if (
    selected_country != "All countries"
    and "country" in filtered_df.columns
):
    filtered_df = filtered_df[
        filtered_df["country"].apply(
            lambda value: contains_country(
                value,
                selected_country
            )
        )
    ]

if (
    selected_ratings
    and "rating" in filtered_df.columns
):
    filtered_df = filtered_df[
        filtered_df["rating"].isin(selected_ratings)
    ]


with st.sidebar:
    st.divider()

    st.metric(
        "Records in current view",
        f"{len(filtered_df):,}"
    )

    st.caption(
        "All charts update automatically."
    )


# =========================================================
# SHARED CALCULATIONS
# =========================================================

type_counts = (
    filtered_df["type"]
    .fillna("Not provided")
    .astype(str)
    .value_counts()
)

release_year_counts = (
    filtered_df["release_year"]
    .dropna()
    .astype(int)
    .value_counts()
    .sort_index()
)

genre_counts = (
    split_and_count(filtered_df["listed_in"])
    if "listed_in" in filtered_df.columns
    else pd.Series(dtype="int64")
)

country_counts = (
    split_and_count(filtered_df["country"])
    if "country" in filtered_df.columns
    else pd.Series(dtype="int64")
)

movie_count = int(
    filtered_df["type"]
    .fillna("")
    .astype(str)
    .str.casefold()
    .eq("movie")
    .sum()
)

show_count = int(
    filtered_df["type"]
    .fillna("")
    .astype(str)
    .str.casefold()
    .eq("tv show")
    .sum()
)

identified_total = movie_count + show_count

movie_share = (
    movie_count / identified_total * 100
    if identified_total
    else 0
)

if release_year_counts.empty:
    year_coverage = "No data"
else:
    year_coverage = (
        f"{release_year_counts.index.min()}–"
        f"{release_year_counts.index.max()}"
    )


# =========================================================
# QUALITY CALCULATIONS
# =========================================================

important_columns = [
    column
    for column in [
        "title",
        "type",
        "release_year",
        "rating",
        "country",
        "duration",
        "listed_in",
        "description"
    ]
    if column in df.columns
]

if important_columns:
    completeness = (
        1
        - df[important_columns]
        .isna()
        .sum()
        .sum()
        / (
            len(df)
            * len(important_columns)
        )
    )
else:
    completeness = 0

duplicate_count = int(
    df[source_columns].duplicated().sum()
)

quality_score = round(
    max(
        0,
        min(
            100,
            completeness * 100
        )
    )
)


# =========================================================
# EXPLANATION
# =========================================================

st.success(
    f"Current filters return {len(filtered_df):,} records."
)

st.markdown(
    """
    <div class="project-notice">
        <strong>How to interpret this dashboard:</strong>
        one record means one row in the dataset. The results
        describe catalog entries—not viewers, streams, watch
        time, revenue, retention, or title popularity.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TABS
# =========================================================

overview_tab, discover_tab, quality_tab, about_tab = st.tabs(
    [
        "📊 Overview",
        "✨ Discover",
        "🧪 Data Quality",
        "📘 About"
    ]
)


# =========================================================
# OVERVIEW
# =========================================================

with overview_tab:
    st.header("Catalog overview")

    metric_one, metric_two, metric_three, metric_four = (
        st.columns(4)
    )

    metric_one.metric(
        "Catalog records",
        f"{len(filtered_df):,}",
        f"{len(filtered_df) / len(df):.1%} of dataset"
    )

    metric_two.metric(
        "Movie share",
        f"{movie_share:.1f}%",
        f"{movie_count:,} movies"
    )

    metric_three.metric(
        "Country labels",
        f"{len(country_counts):,}"
    )

    metric_four.metric(
        "Release years",
        year_coverage
    )

    if filtered_df.empty:
        st.warning(
            "No records match the filters. "
            "Change the sidebar selections."
        )

    else:
        st.subheader("Automatic findings")

        finding_one, finding_two, finding_three = st.columns(3)

        with finding_one:
            with st.container(border=True):
                st.caption("CONTENT MIX")

                if movie_count >= show_count:
                    st.subheader("Movies lead")
                else:
                    st.subheader("TV shows lead")

                st.write(
                    f"{movie_count:,} movie records and "
                    f"{show_count:,} TV-show records appear "
                    f"in the current view."
                )

        with finding_two:
            with st.container(border=True):
                st.caption("PEAK RELEASE YEAR")

                if not release_year_counts.empty:
                    peak_year = int(
                        release_year_counts.idxmax()
                    )

                    peak_count = int(
                        release_year_counts.max()
                    )

                    st.subheader(str(peak_year))

                    st.write(
                        f"{peak_count:,} records are associated "
                        f"with this release year."
                    )

        with finding_three:
            with st.container(border=True):
                st.caption("TOP GENRE LABEL")

                if not genre_counts.empty:
                    top_genre = genre_counts.index[0]
                    top_count = int(genre_counts.iloc[0])

                    st.subheader(top_genre)

                    st.write(
                        f"This label appears in "
                        f"{top_count:,} records."
                    )

        left_chart, right_chart = st.columns(2)

        with left_chart:
            st.subheader("Movie and TV-show mix")

            type_data = (
                type_counts
                .rename_axis("Content type")
                .reset_index(name="Records")
            )

            type_figure = px.pie(
                type_data,
                names="Content type",
                values="Records",
                hole=0.68,
                color_discrete_sequence=CHART_COLORS
            )

            type_figure.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "%{value:,} records<br>"
                    "%{percent}"
                    "<extra></extra>"
                )
            )

            type_figure.update_layout(showlegend=False)

            style_chart(type_figure)

            st.plotly_chart(
                type_figure,
                use_container_width=True,
                theme=None,
                config=PLOT_CONFIG
            )

        with right_chart:
            st.subheader("Records by release year")

            year_data = (
                release_year_counts
                .rename_axis("Release year")
                .reset_index(name="Records")
            )

            year_figure = px.area(
                year_data,
                x="Release year",
                y="Records"
            )

            year_figure.update_traces(
                line_color=CORAL,
                fillcolor="rgba(255,122,107,0.18)",
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "%{y:,} records"
                    "<extra></extra>"
                )
            )

            style_chart(year_figure)

            st.plotly_chart(
                year_figure,
                use_container_width=True,
                theme=None,
                config=PLOT_CONFIG
            )

        genre_column, country_column = st.columns(2)

        with genre_column:
            st.subheader("Genre landscape")

            if genre_counts.empty:
                st.info("Genre data is unavailable.")

            else:
                genre_data = (
                    genre_counts
                    .head(20)
                    .rename_axis("Genre")
                    .reset_index(name="Records")
                )

                genre_figure = px.treemap(
                    genre_data,
                    path=["Genre"],
                    values="Records",
                    color="Records",
                    color_continuous_scale=[
                        "#3E2228",
                        CORAL,
                        GOLD
                    ]
                )

                genre_figure.update_traces(
                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "%{value:,} records"
                        "<extra></extra>"
                    )
                )

                style_chart(genre_figure, 440)

                st.plotly_chart(
                    genre_figure,
                    use_container_width=True,
                    theme=None,
                    config=PLOT_CONFIG
                )

        with country_column:
            st.subheader("Frequent country labels")

            if country_counts.empty:
                st.info("Country data is unavailable.")

            else:
                country_data = (
                    country_counts
                    .head(12)
                    .sort_values()
                    .rename_axis("Country")
                    .reset_index(name="Records")
                )

                country_figure = px.bar(
                    country_data,
                    x="Records",
                    y="Country",
                    orientation="h",
                    color="Records",
                    color_continuous_scale=[
                        "#4B3031",
                        CORAL,
                        GOLD
                    ]
                )

                country_figure.update_layout(
                    coloraxis_showscale=False
                )

                style_chart(country_figure, 440)

                st.plotly_chart(
                    country_figure,
                    use_container_width=True,
                    theme=None,
                    config=PLOT_CONFIG
                )


# =========================================================
# DISCOVER
# =========================================================

with discover_tab:
    st.header("Title discovery")

    title_options = sorted(
        filtered_df["title"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if not title_options:
        st.warning(
            "No titles match the current filters."
        )

    else:
        selected_title = st.selectbox(
            "Choose a title",
            options=title_options
        )

        selected_record = (
            filtered_df[
                filtered_df["title"] == selected_title
            ]
            .iloc[0]
        )

        detail_one, detail_two = st.columns([1.5, 1])

        with detail_one:
            with st.container(border=True):
                st.caption("SELECTED TITLE")

                st.subheader(selected_title)

                st.write(
                    readable(
                        selected_record.get("description"),
                        "No description is available."
                    )
                )

        with detail_two:
            with st.container(border=True):
                st.caption("TITLE DETAILS")

                st.write(
                    "**Type:**",
                    readable(selected_record.get("type"))
                )

                st.write(
                    "**Release year:**",
                    readable(
                        selected_record.get("release_year")
                    )
                )

                st.write(
                    "**Rating:**",
                    readable(selected_record.get("rating"))
                )

                st.write(
                    "**Duration:**",
                    readable(selected_record.get("duration"))
                )

                st.write(
                    "**Genres:**",
                    readable(selected_record.get("listed_in"))
                )

        recommendations = create_recommendations(
            filtered_df if len(filtered_df) >= 7 else df,
            selected_title
        )

        st.subheader(
            f"Related to “{selected_title}”"
        )

        st.caption(
            "Suggestions use shared genres, content type, "
            "rating, and nearby release years."
        )

        if recommendations.empty:
            st.info("No related titles were found.")

        else:
            recommendation_columns = st.columns(3)

            for position, (_, row) in enumerate(
                recommendations.iterrows()
            ):
                with recommendation_columns[position % 3]:
                    with st.container(border=True):
                        st.caption(
                            "MATCH SCORE · "
                            f"{int(row['_recommendation_score'])}"
                        )

                        st.subheader(
                            readable(row.get("title"))
                        )

                        st.write(
                            readable(row.get("type")),
                            "•",
                            readable(row.get("release_year"))
                        )

                        st.caption(
                            readable(
                                row.get("listed_in"),
                                "Genres unavailable"
                            )
                        )

        st.divider()

        st.subheader("🎲 Surprise Me")

        if (
            "random_title" not in st.session_state
            or st.session_state.random_title
            not in title_options
        ):
            st.session_state.random_title = title_options[0]

        if st.button(
            "Choose a random title",
            type="primary"
        ):
            st.session_state.random_title = random.choice(
                title_options
            )

        random_title = st.session_state.random_title

        random_record = (
            filtered_df[
                filtered_df["title"] == random_title
            ]
            .iloc[0]
        )

        with st.container(border=True):
            st.caption("RANDOM DISCOVERY")

            st.subheader(random_title)

            st.write(
                readable(
                    random_record.get("description"),
                    "No description is available."
                )
            )

            st.write(
                "**Genres:**",
                readable(random_record.get("listed_in"))
            )


# =========================================================
# DATA QUALITY
# =========================================================

with quality_tab:
    st.header("Data-quality analysis")

    gauge_column, metrics_column = st.columns([1.1, 1])

    with gauge_column:
        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=quality_score,
                number={
                    "suffix": "/100",
                    "font": {
                        "color": TEXT,
                        "size": 42
                    }
                },
                title={
                    "text": "Dataset completeness estimate",
                    "font": {
                        "color": MUTED,
                        "size": 16
                    }
                },
                gauge={
                    "axis": {
                        "range": [0, 100],
                        "tickcolor": MUTED
                    },
                    "bar": {
                        "color": CORAL
                    },
                    "bgcolor": PANEL,
                    "bordercolor": BORDER,
                    "steps": [
                        {
                            "range": [0, 50],
                            "color": "#3A2025"
                        },
                        {
                            "range": [50, 80],
                            "color": "#403720"
                        },
                        {
                            "range": [80, 100],
                            "color": "#234036"
                        }
                    ]
                }
            )
        )

        style_chart(gauge, 350)

        st.plotly_chart(
            gauge,
            use_container_width=True,
            theme=None,
            config=PLOT_CONFIG
        )

        st.caption(
            "This is a project-specific completeness estimate, "
            "not an official industry standard."
        )

    with metrics_column:
        first_metric, second_metric = st.columns(2)

        first_metric.metric(
            "Dataset records",
            f"{len(df):,}"
        )

        second_metric.metric(
            "Exact duplicates",
            f"{duplicate_count:,}"
        )

        third_metric, fourth_metric = st.columns(2)

        third_metric.metric(
            "Completeness",
            f"{completeness * 100:.1f}%"
        )

        fourth_metric.metric(
            "Columns analyzed",
            f"{len(source_columns):,}"
        )

        st.info(
            "The application reports missing values and "
            "duplicates without automatically deleting rows."
        )

    st.subheader("Missing values by column")

    missing_data = pd.DataFrame(
        {
            "Column": source_columns,
            "Missing values": [
                int(df[column].isna().sum())
                for column in source_columns
            ],
            "Missing percentage": [
                round(
                    df[column].isna().mean() * 100,
                    2
                )
                for column in source_columns
            ]
        }
    ).sort_values(
        "Missing values",
        ascending=False
    )

    st.dataframe(
        missing_data,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Explore current records")

    display_columns = [
        column
        for column in [
            "title",
            "type",
            "release_year",
            "rating",
            "country",
            "duration",
            "listed_in",
            "director",
            "date_added"
        ]
        if column in filtered_df.columns
    ]

    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        height=500,
        hide_index=True
    )

    download_data = (
        filtered_df[source_columns]
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "Download filtered records",
        data=download_data,
        file_name="netflix_filtered_records.csv",
        mime="text/csv",
        type="primary",
        use_container_width=True
    )


# =========================================================
# ABOUT
# =========================================================

with about_tab:
    st.header("About this project")

    st.write(
        """
        Netflix Analytics Studio is an independent project that
        demonstrates an end-to-end analytics workflow: loading a
        dataset, preparing its fields, checking its quality,
        building interactive visualizations, applying filters,
        and communicating findings and limitations.
        """
    )

    st.subheader("Questions explored")

    st.markdown(
        """
        1. How are records divided between movies and TV shows?
        2. Which release years appear most frequently?
        3. Which genres and country labels occur often?
        4. Which fields contain missing information?
        5. Can transparent rules identify related titles?
        """
    )

    st.subheader("Recommendation method")

    recommendation_rules = pd.DataFrame(
        {
            "Rule": [
                "Shared genre",
                "Same content type",
                "Same rating",
                "Released within 3 years",
                "Released within 10 years"
            ],
            "Points": [
                "4 per genre",
                "2",
                "1",
                "2",
                "1"
            ]
        }
    )

    st.dataframe(
        recommendation_rules,
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "The recommendations are rule-based. They do not "
        "reproduce Netflix's actual recommendation system."
    )

    st.subheader("Limitations")

    st.markdown(
        """
        - The dataset is a static snapshot.
        - Records do not represent viewers or streams.
        - The analysis does not measure popularity or revenue.
        - Country and genre counts can overlap.
        - Missing values can affect some comparisons.
        - Release year is different from date added.
        """
    )

    st.subheader("Skills demonstrated")

    st.markdown(
        """
        - Python application development
        - Pandas data preparation
        - Plotly data visualization
        - Streamlit dashboard development
        - Data-quality reporting
        - Dynamic filters
        - Rule-based recommendation logic
        - Data storytelling
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <footer class="project-footer">
        Netflix Analytics Studio<br>
        Completed independent project by Ummi Habiba<br>
        Python · Pandas · Plotly · Streamlit<br>
        Not affiliated with Netflix
    </footer>
    """,
    unsafe_allow_html=True
)