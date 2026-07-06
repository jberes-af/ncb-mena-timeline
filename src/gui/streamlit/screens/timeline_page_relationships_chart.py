# /src/gui/screens/timeline_page_relationships_chart.py

import pandas as pd
import streamlit as st

from src.application.dto.dataset_analytics_dtos import (
    ActorPairCountDTO,
)


def render_actor_pair_counts_chart(
        *,
        pair_counts: tuple[ActorPairCountDTO, ...],
        max_pairs: int = 10,
) -> None:
    if not pair_counts:
        return

    top_pairs = sorted(
        pair_counts,
        key=lambda pair: pair.count,
        reverse=True,
    )[:max_pairs]

    chart_df = pd.DataFrame(
        [
            {
                "Relationship": (
                    f"{pair.actor_1_label} + {pair.actor_2_label}"
                ),
                "Events": pair.count,
            }
            for pair in top_pairs
        ]
    )

    with st.expander("Most Common Pairs", expanded=False):
        st.write(
            "Actor pairs that appear together most often in the selected timeline."
        )

        st.bar_chart(
            chart_df,
            x="Relationship",
            y="Events",
            horizontal=True,
            use_container_width=True,
        )

        st.dataframe(
            chart_df,
            use_container_width=True,
            hide_index=True,
        )
