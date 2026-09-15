import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Social Media Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    font-size: 17px;
    color: #6b7280;
    margin-bottom: 25px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #111827;
    margin-top: 30px;
    margin-bottom: 15px;
}

.kpi-card {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
}

.kpi-label {
    font-size: 14px;
    color: #6b7280;
    font-weight: 600;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #111827;
}

.kpi-icon {
    font-size: 24px;
    margin-bottom: 5px;
}

.insight-card {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 15px;
    padding: 20px;
    min-height: 150px;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
}

.insight-title {
    font-size: 14px;
    color: #6b7280;
    font-weight: 600;
    margin-bottom: 10px;
}

.insight-main {
    font-size: 22px;
    font-weight: 800;
    color: #111827;
}

.insight-detail {
    font-size: 14px;
    color: #6b7280;
    margin-top: 8px;
}

.recommendation-box {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-left: 5px solid #111827;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 12px;
    color: #374151;
    font-size: 15px;
}

.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 13px;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #e5e7eb;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("data/social_media_data.csv")


# ============================================================
# DATA CLEANING & FEATURE ENGINEERING
# ============================================================

df["date"] = pd.to_datetime(df["date"])

df["hour"] = pd.to_datetime(
    df["time"],
    format="%H:%M"
).dt.hour

df["day"] = df["date"].dt.day_name()

df["engagement"] = (
    df["likes"]
    + df["comments"]
    + df["shares"]
)

df["engagement_rate"] = (
    df["engagement"] / df["views"]
) * 100

df = df.sort_values("date").reset_index(drop=True)

df["follower_growth"] = df["followers"].diff()

df["hashtags"] = df["hashtags"].str.split()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 📊 Analytics")

    st.caption(
        "Social Media Performance Dashboard"
    )

    st.markdown("---")

    st.markdown("### 🎛️ Filters")


    # --------------------------------------------------------
    # PLATFORM FILTER
    # --------------------------------------------------------

    platform_options = [
        "All"
    ] + sorted(
        df["platform"].unique().tolist()
    )

    selected_platform = st.selectbox(
        "📱 Platform",
        platform_options
    )


    # --------------------------------------------------------
    # CONTENT TYPE FILTER
    # --------------------------------------------------------

    content_options = [
        "All"
    ] + sorted(
        df["content_type"].unique().tolist()
    )

    selected_content = st.selectbox(
        "🎬 Content Type",
        content_options
    )


    # --------------------------------------------------------
    # DATE RANGE FILTER
    # --------------------------------------------------------

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    selected_dates = st.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )


    st.markdown("---")

    st.markdown("### 📌 Dataset")

    st.write(
        f"**Total Posts:** {len(df)}"
    )

    st.write(
        f"**Platforms:** {df['platform'].nunique()}"
    )

    st.write(
        f"**Content Types:** {df['content_type'].nunique()}"
    )

    st.markdown("---")

    st.caption(
        "Built with Python • Pandas • Plotly • Streamlit"
    )


# ============================================================
# HANDLE DATE RANGE
# ============================================================

if isinstance(selected_dates, tuple):

    if len(selected_dates) == 2:

        start_date = pd.to_datetime(
            selected_dates[0]
        )

        end_date = pd.to_datetime(
            selected_dates[1]
        )

    else:

        start_date = pd.to_datetime(
            selected_dates[0]
        )

        end_date = start_date

else:

    start_date = pd.to_datetime(
        selected_dates
    )

    end_date = start_date


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if selected_platform != "All":

    filtered_df = filtered_df[
        filtered_df["platform"] == selected_platform
    ]


if selected_content != "All":

    filtered_df = filtered_df[
        filtered_df["content_type"] == selected_content
    ]


filtered_df = filtered_df[
    (filtered_df["date"] >= start_date)
    &
    (filtered_df["date"] <= end_date)
]


filtered_df = filtered_df.sort_values("date")


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if len(filtered_df) == 0:

    st.warning(
        "No posts match the selected filters. "
        "Please change your filters."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">'
    '📊 Social Media Analytics Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Monitor content performance, engagement, audience growth '
    'and posting trends.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FILTER STATUS
# ============================================================

st.info(
    f"Showing **{len(filtered_df)} posts**  •  "
    f"Platform: **{selected_platform}**  •  "
    f"Content: **{selected_content}**  •  "
    f"Date: **{start_date.strftime('%d %b %Y')}** "
    f"→ **{end_date.strftime('%d %b %Y')}**"
)


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

st.subheader("📥 Export Data")

download_df = filtered_df.copy()

download_df["hashtags"] = (
    download_df["hashtags"]
    .apply(
        lambda x: " ".join(x)
        if isinstance(x, list)
        else x
    )
)

csv_data = download_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download Filtered CSV",
    data=csv_data,
    file_name="filtered_social_media_data.csv",
    mime="text/csv"
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_views = filtered_df["views"].sum()

total_likes = filtered_df["likes"].sum()

total_comments = filtered_df["comments"].sum()

total_shares = filtered_df["shares"].sum()

average_engagement_rate = (
    filtered_df["engagement_rate"].mean()
)

latest_followers = (
    filtered_df
    .sort_values("date")["followers"]
    .iloc[-1]
)


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📈 Performance Overview'
    '</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4, col5, col6 = st.columns(6)


with col1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">👁️</div>
            <div class="kpi-label">TOTAL VIEWS</div>
            <div class="kpi-value">{total_views:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">❤️</div>
            <div class="kpi-label">TOTAL LIKES</div>
            <div class="kpi-value">{total_likes:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">💬</div>
            <div class="kpi-label">COMMENTS</div>
            <div class="kpi-value">{total_comments:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🔄</div>
            <div class="kpi-label">SHARES</div>
            <div class="kpi-value">{total_shares:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col5:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">FOLLOWERS</div>
            <div class="kpi-value">{latest_followers:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col6:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">📈</div>
            <div class="kpi-label">ENGAGEMENT RATE</div>
            <div class="kpi-value">
                {average_engagement_rate:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DATASET
# ============================================================

with st.expander("📋 View Filtered Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PLATFORM ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📊 Platform Analysis'
    '</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    platform_views = (
        filtered_df
        .groupby("platform")["views"]
        .mean()
        .reset_index()
    )

    fig_platform = px.bar(
        platform_views,
        x="platform",
        y="views",
        title="Average Views by Platform",
        text_auto=".2s"
    )

    fig_platform.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_platform,
        use_container_width=True
    )


with col2:

    platform_engagement = (
        filtered_df
        .groupby("platform")["engagement_rate"]
        .mean()
        .reset_index()
    )

    fig_engagement = px.bar(
        platform_engagement,
        x="platform",
        y="engagement_rate",
        title="Average Engagement Rate by Platform",
        text_auto=".2f"
    )

    fig_engagement.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_engagement,
        use_container_width=True
    )


# ============================================================
# CONTENT & TIMING
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🎬 Content & Timing'
    '</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    content_performance = (
        filtered_df
        .groupby("content_type")["engagement_rate"]
        .mean()
        .reset_index()
        .sort_values(
            "engagement_rate",
            ascending=False
        )
    )

    fig_content = px.bar(
        content_performance,
        x="content_type",
        y="engagement_rate",
        title="Engagement Rate by Content Type",
        text_auto=".2f"
    )

    fig_content.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_content,
        use_container_width=True
    )


with col2:

    day_performance = (
        filtered_df
        .groupby("day")["engagement_rate"]
        .mean()
        .reset_index()
        .sort_values(
            "engagement_rate",
            ascending=False
        )
    )

    fig_day = px.bar(
        day_performance,
        x="day",
        y="engagement_rate",
        title="Average Engagement Rate by Day",
        text_auto=".2f"
    )

    fig_day.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_day,
        use_container_width=True
    )


# ============================================================
# TIME ANALYSIS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    hour_performance = (
        filtered_df
        .groupby("hour")["engagement_rate"]
        .mean()
        .reset_index()
        .sort_values("hour")
    )

    fig_hour = px.line(
        hour_performance,
        x="hour",
        y="engagement_rate",
        markers=True,
        title="Engagement Rate by Posting Hour"
    )

    fig_hour.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_hour,
        use_container_width=True
    )


with col2:

    engagement_time = (
        filtered_df
        .sort_values("date")
    )

    fig_time = px.line(
        engagement_time,
        x="date",
        y="engagement_rate",
        markers=True,
        title="Engagement Rate Over Time"
    )

    fig_time.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_time,
        use_container_width=True
    )


# ============================================================
# TOP & BOTTOM POSTS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🏆 Best & Weakest Content'
    '</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    top_posts = (
        filtered_df
        .sort_values(
            "engagement_rate",
            ascending=False
        )
        .head(5)
    )

    fig_top = px.bar(
        top_posts,
        x="caption",
        y="engagement_rate",
        color="platform",
        title="Top 5 Performing Posts",
        text_auto=".2f"
    )

    fig_top.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_top,
        use_container_width=True
    )


with col2:

    bottom_posts = (
        filtered_df
        .sort_values(
            "engagement_rate",
            ascending=True
        )
        .head(5)
    )

    fig_bottom = px.bar(
        bottom_posts,
        x="caption",
        y="engagement_rate",
        color="platform",
        title="Bottom 5 Performing Posts",
        text_auto=".2f"
    )

    fig_bottom.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_bottom,
        use_container_width=True
    )


# ============================================================
# ENGAGEMENT ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔎 Engagement Analysis'
    '</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    fig_scatter = px.scatter(
        filtered_df,
        x="views",
        y="engagement_rate",
        hover_data=[
            "platform",
            "content_type",
            "caption"
        ],
        title="Views vs Engagement Rate"
    )

    fig_scatter.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )


with col2:

    engagement_components = (
        filtered_df
        .groupby("platform")[
            [
                "likes",
                "comments",
                "shares"
            ]
        ]
        .mean()
        .reset_index()
    )

    fig_components = px.bar(
        engagement_components,
        x="platform",
        y=[
            "likes",
            "comments",
            "shares"
        ],
        barmode="group",
        title="Average Likes, Comments & Shares"
    )

    fig_components.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_components,
        use_container_width=True
    )


# ============================================================
# HASHTAG PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">'
    '#️⃣ Hashtag Performance'
    '</div>',
    unsafe_allow_html=True
)


hashtag_performance = (
    filtered_df
    .explode("hashtags")
    .groupby("hashtags")["engagement_rate"]
    .mean()
    .sort_values(
        ascending=False
    )
    .head(5)
    .reset_index()
)


fig_hashtags = px.bar(
    hashtag_performance,
    x="hashtags",
    y="engagement_rate",
    title="Top 5 Hashtags by Average Engagement Rate",
    text_auto=".2f"
)


fig_hashtags.update_layout(
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    ),
    plot_bgcolor="white",
    paper_bgcolor="white"
)


st.plotly_chart(
    fig_hashtags,
    use_container_width=True
)


# ============================================================
# AUDIENCE GROWTH
# ============================================================

st.markdown(
    '<div class="section-title">'
    '👥 Audience Growth'
    '</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    fig_followers = px.line(
        filtered_df.sort_values("date"),
        x="date",
        y="followers",
        markers=True,
        title="Follower Growth Over Time"
    )

    fig_followers.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(
        fig_followers,
        use_container_width=True
    )


with col2:

    follower_growth_df = filtered_df[
        filtered_df["follower_growth"].notna()
    ]

    if len(follower_growth_df) > 0:

        fig_growth = px.bar(
            follower_growth_df,
            x="caption",
            y="follower_growth",
            color="platform",
            title="Follower Growth per Post",
            text_auto=True
        )

        fig_growth.update_layout(
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            ),
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig_growth,
            use_container_width=True
        )

    else:

        st.info(
            "Not enough data to calculate follower growth."
        )


# ============================================================
# AUTOMATED DATA INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '💡 Automated Data Insights'
    '</div>',
    unsafe_allow_html=True
)


platform_rates = (
    filtered_df
    .groupby("platform")["engagement_rate"]
    .mean()
    .sort_values(ascending=False)
)

best_platform = platform_rates.index[0]

best_platform_rate = platform_rates.iloc[0]


content_rates = (
    filtered_df
    .groupby("content_type")["engagement_rate"]
    .mean()
    .sort_values(ascending=False)
)

best_content = content_rates.index[0]

best_content_rate = content_rates.iloc[0]


day_rates = (
    filtered_df
    .groupby("day")["engagement_rate"]
    .mean()
    .sort_values(ascending=False)
)

best_day = day_rates.index[0]

best_day_rate = day_rates.iloc[0]


hour_rates = (
    filtered_df
    .groupby("hour")["engagement_rate"]
    .mean()
    .sort_values(ascending=False)
)

best_hour = hour_rates.index[0]

best_hour_rate = hour_rates.iloc[0]


weakest_content = content_rates.index[-1]

weakest_content_rate = content_rates.iloc[-1]


# ============================================================
# INSIGHT CARDS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">
                🏆 BEST PLATFORM
            </div>

            <div class="insight-main">
                {best_platform}
            </div>

            <div class="insight-detail">
                Engagement Rate:
                {best_platform_rate:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">
                🎬 BEST CONTENT TYPE
            </div>

            <div class="insight-main">
                {best_content}
            </div>

            <div class="insight-detail">
                Engagement Rate:
                {best_content_rate:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">
                📅 BEST POSTING DAY
            </div>

            <div class="insight-main">
                {best_day}
            </div>

            <div class="insight-detail">
                Engagement Rate:
                {best_day_rate:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


col4, col5, col6 = st.columns(3)


with col4:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">
                ⏰ BEST POSTING HOUR
            </div>

            <div class="insight-main">
                {best_hour}:00
            </div>

            <div class="insight-detail">
                Engagement Rate:
                {best_hour_rate:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col5:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">
                ⚠️ WEAKEST CONTENT TYPE
            </div>

            <div class="insight-main">
                {weakest_content}
            </div>

            <div class="insight-detail">
                Engagement Rate:
                {weakest_content_rate:.2f}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col6:

    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">
                📈 AVERAGE ENGAGEMENT
            </div>

            <div class="insight-main">
                {filtered_df["engagement_rate"].mean():.2f}%
            </div>

            <div class="insight-detail">
                Across selected posts
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🚀 Recommendations'
    '</div>',
    unsafe_allow_html=True
)


recommendations = [

    f"📱 <b>Platform:</b> {best_platform} is currently the strongest "
    f"platform with an average engagement rate of "
    f"<b>{best_platform_rate:.2f}%</b>.",

    f"🎬 <b>Content:</b> {best_content} content is performing best "
    f"with an average engagement rate of "
    f"<b>{best_content_rate:.2f}%</b>.",

    f"📅 <b>Day:</b> {best_day} is the strongest posting day "
    f"based on average engagement rate.",

    f"⏰ <b>Time:</b> The strongest posting hour is around "
    f"<b>{best_hour}:00</b>.",

    f"💡 <b>Strategy:</b> Consider creating more "
    f"<b>{best_content}</b> content and testing posts around "
    f"<b>{best_hour}:00 on {best_day}</b>.",

    f"⚠️ <b>Improvement Area:</b> {weakest_content} currently "
    f"has the lowest average engagement rate at "
    f"<b>{weakest_content_rate:.2f}%</b>."
]


for recommendation in recommendations:

    st.markdown(
        f"""
        <div class="recommendation-box">
            {recommendation}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        📊 Social Media Analytics Dashboard
        <br>
        Built with Python • Pandas • Plotly • Streamlit
    </div>
    """,
    unsafe_allow_html=True
)

