import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from src.inference import load_models, predict_rf, predict_tier2, predict_tier3
from src.visualization import render_attention_heatmap_html
from src.sample_queries import get_sample_queries

st.set_page_config(
    page_title="SQL Injection Detection Middleware",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --soc-bg: #f8fafc;
        --soc-surface: #ffffff;
        --soc-border: #e2e8f0;
        --soc-text-primary: #0f172a;
        --soc-text-secondary: #475569;
        --soc-text-muted: #94a3b8;
        --soc-danger-bg: #fef2f2;
        --soc-danger-border: #fecaca;
        --soc-danger-text: #b91c1c;
        --soc-success-bg: #f0fdf4;
        --soc-success-border: #bbf7d0;
        --soc-success-text: #15803d;
        --soc-mono: ui-monospace, SFMono-Regular, "Roboto Mono", Menlo, Consolas, monospace;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    /* KHÔNG có "header {visibility: hidden;}" ở đây -- giữ header để nút
       thu gọn/mở sidebar (<< và >>) vẫn hoạt động bình thường */

    .block-container {
        padding-top: 4.5rem;
        padding-bottom: 2rem;
        max-width: 1180px;
    }

    body, .stApp {
        background-color: var(--soc-bg);
        color: var(--soc-text-primary);
    }

    hr {
        margin-top: 0.9rem;
        margin-bottom: 0.9rem;
        border-color: var(--soc-border);
    }

    /* --- Header bảng điều khiển --- */
    .soc-header-title {
        font-size: 26px;
        font-weight: 700;
        color: var(--soc-text-primary);
        letter-spacing: -0.01em;
        margin: 0;
    }
    .soc-header-subtitle {
        font-size: 14px;
        color: var(--soc-text-secondary);
        margin-top: 6px;
        line-height: 1.5;
        max-width: 720px;
    }

    /* --- Dải sơ đồ luồng xử lý (thay cho badge trạng thái đơn lẻ) --- */
    .soc-flow {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 14px;
    }
    .soc-flow-step {
        font-family: var(--soc-mono);
        font-size: 12px;
        font-weight: 600;
        color: var(--soc-text-secondary);
        background: #f1f5f9;
        border: 1px solid var(--soc-border);
        border-radius: 4px;
        padding: 6px 12px;
        white-space: nowrap;
    }
    .soc-flow-step-active {
        color: var(--soc-text-primary);
        background: #eff6ff;
        border-color: #bfdbfe;
    }
    .soc-flow-arrow {
        color: var(--soc-text-muted);
        font-size: 13px;
    }

    /* --- Nhãn khu vực --- */
    .soc-section-label {
        font-size: 15px;
        font-weight: 600;
        color: var(--soc-text-primary);
        margin-bottom: 2px;
    }
    .soc-section-caption {
        font-size: 13px;
        color: var(--soc-text-muted);
        margin-bottom: 10px;
    }

    /* --- Thẻ kết quả mô hình --- */
    .model-card {
        border: 1px solid var(--soc-border);
        border-radius: 6px;
        padding: 14px;
        background: var(--soc-surface);
    }
    .model-card-name {
        font-size: 13px;
        font-weight: 600;
        color: var(--soc-text-secondary);
        margin-bottom: 10px;
    }
    .model-badge {
        display: inline-block;
        font-family: var(--soc-mono);
        font-size: 12.5px;
        font-weight: 600;
        border-radius: 4px;
        padding: 4px 10px;
        border: 1px solid;
        margin-bottom: 12px;
    }
    .model-badge-blocked {
        color: var(--soc-danger-text);
        background: var(--soc-danger-bg);
        border-color: var(--soc-danger-border);
    }
    .model-badge-clean {
        color: var(--soc-success-text);
        background: var(--soc-success-bg);
        border-color: var(--soc-success-border);
    }
    .model-confidence {
        font-size: 26px;
        font-weight: 700;
        color: var(--soc-text-primary);
        line-height: 1.1;
    }
    .model-confidence-label {
        font-size: 11.5px;
        color: var(--soc-text-muted);
        margin-bottom: 2px;
    }
    .model-latency {
        font-family: var(--soc-mono);
        font-size: 11.5px;
        color: var(--soc-text-muted);
        margin-top: 10px;
    }

    /* --- Legend heatmap attention --- */
    .attn-legend {
        display: flex;
        align-items: center;
        margin-top: 8px;
    }
    .attn-legend-label {
        font-family: var(--soc-mono);
        font-size: 10.5px;
        color: var(--soc-text-muted);
        white-space: nowrap;
    }
    .attn-legend-bar {
        flex: 1;
        height: 6px;
        border-radius: 3px;
        margin: 0 8px;
        background: linear-gradient(to right, #eff6ff, #1d4ed8);
    }

    /* --- KPI panel sidebar --- */
    .kpi-panel {
        border: 1px solid var(--soc-border);
        border-radius: 6px;
        background: var(--soc-surface);
        padding: 14px;
    }
    .kpi-panel-title {
        font-family: var(--soc-mono);
        font-size: 11.5px;
        color: var(--soc-text-muted);
        margin-bottom: 10px;
    }
    .kpi-row {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        padding: 7px 0;
        border-top: 1px solid var(--soc-border);
    }
    .kpi-row:first-of-type {
        border-top: none;
    }
    .kpi-label {
        font-size: 12.5px;
        color: var(--soc-text-secondary);
    }
    .kpi-value {
        font-family: var(--soc-mono);
        font-size: 14px;
        font-weight: 600;
        color: var(--soc-text-primary);
    }
    .kpi-value-sub {
        font-size: 11.5px;
        font-weight: 400;
        color: var(--soc-text-muted);
    }
    .kpi-note {
        font-size: 11px;
        color: var(--soc-text-muted);
        margin-top: 10px;
        line-height: 1.4;
    }
        /* --- Banner tóm tắt đồng thuận giữa 3 model --- */
    .consensus-banner {
        margin-top: 20px;
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 13.5px;
        font-weight: 600;
        border: 1px solid;
    }
    .consensus-full-sqli {
        background: var(--soc-danger-bg);
        border-color: var(--soc-danger-border);
        color: var(--soc-danger-text);
    }
    .consensus-full-clean {
        background: var(--soc-success-bg);
        border-color: var(--soc-success-border);
        color: var(--soc-success-text);
    }
    .consensus-majority {
        background: #fffbeb;
        border-color: #fde68a;
        color: #92400e;
    }
    .consensus-none {
        background: #f1f5f9;
        border-color: var(--soc-border);
        color: var(--soc-text-secondary);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p class="soc-header-title">SQL Injection Detection Middleware</p>
    <p class="soc-header-subtitle">
        Hệ thống phân tích truy vấn thời gian thực · Kiến trúc 3 tầng:
        Random Forest (Features) | LSTM Baseline | LSTM + Additive Attention
    </p>
    <div class="soc-flow">
        <span class="soc-flow-step">INPUT</span>
        <span class="soc-flow-arrow">&rarr;</span>
        <span class="soc-flow-step">INSPECT (3 MODELS)</span>
        <span class="soc-flow-arrow">&rarr;</span>
        <span class="soc-flow-step soc-flow-step-active">ALLOW / BLOCK</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()


@st.cache_resource
def get_models():
    with st.spinner("Đang load 3 model lần đầu (Tier 2/3 mất vài giây)..."):
        return load_models()


models = get_models()


def render_session_stats():
    history = st.session_state.get("history", [])
    total = len(history)
    flagged_any = sum(
        1 for h in history if any(r["label"] == 1 for r in h["results"].values())
    )
    flagged_all = sum(
        1 for h in history if all(r["label"] == 1 for r in h["results"].values())
    )
    pct_any = (flagged_any / total * 100) if total > 0 else 0.0
    pct_all = (flagged_all / total * 100) if total > 0 else 0.0

    st.sidebar.markdown(
        f"""
        <div class="kpi-panel">
            <div class="kpi-panel-title">THỐNG KÊ PHIÊN LÀM VIỆC</div>
            <div class="kpi-row">
                <span class="kpi-label">Tổng truy vấn đã quét</span>
                <span class="kpi-value">{total}</span>
            </div>
            <div class="kpi-row">
                <span class="kpi-label">Bị chặn (≥1 model)</span>
                <span class="kpi-value">{flagged_any} <span class="kpi-value-sub">({pct_any:.1f}%)</span></span>
            </div>
            <div class="kpi-row">
                <span class="kpi-label">Đồng thuận cả 3 mô hình</span>
                <span class="kpi-value">{flagged_all} <span class="kpi-value-sub">({pct_all:.1f}%)</span></span>
            </div>
        </div>
        <div class="kpi-note">
            Lưu ý: Dữ liệu thống kê duy trì theo phiên làm việc (Session Scope) —
            mất khi tải lại trang (F5).
        </div>
        """,
        unsafe_allow_html=True,
    )
def _render_consensus_banner(results: dict):
    total = len(results)
    sqli_count = sum(1 for r in results.values() if r["label"] == 1)
    clean_count = total - sqli_count

    if sqli_count == total:
        css_class = "consensus-full-sqli"
        text = "Đồng thuận hoàn toàn — cả 3 mô hình đều xác định đây là SQL Injection."
    elif clean_count == total:
        css_class = "consensus-full-clean"
        text = "Đồng thuận hoàn toàn — cả 3 mô hình đều xác định đây là truy vấn hợp lệ."
    elif sqli_count > clean_count:
        css_class = "consensus-majority"
        text = (
            f"Đa số đồng thuận ({sqli_count}/{total}) — phần lớn mô hình nghiêng về "
            "SQL Injection, chưa có sự thống nhất tuyệt đối."
        )
    elif clean_count > sqli_count:
        css_class = "consensus-majority"
        text = (
            f"Đa số đồng thuận ({clean_count}/{total}) — phần lớn mô hình nghiêng về "
            "Hợp lệ, chưa có sự thống nhất tuyệt đối."
        )
    else:
        css_class = "consensus-none"
        text = (
            "Không đồng thuận — các mô hình đưa ra kết quả trái ngược nhau, "
            "không có bên nào chiếm đa số."
        )

    st.markdown(
        f'<div class="consensus-banner {css_class}">{text}</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="soc-section-label">Truy vấn mẫu</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="soc-section-caption">Nạp nhanh một truy vấn từ tập kiểm thử độc lập.</div>',
    unsafe_allow_html=True,
)

sample_queries = get_sample_queries()
placeholder_label = "-- Chọn truy vấn mẫu từ tập kiểm thử độc lập (Benchmark Test Set) --"
sample_option_labels = [placeholder_label] + [s["label_ui"] for s in sample_queries]
label_to_query = {s["label_ui"]: s["query"] for s in sample_queries}

select_col, button_col = st.columns([4, 1])
with select_col:
    selected_sample_label = st.selectbox(
        "Truy vấn mẫu",
        options=sample_option_labels,
        key="sample_select",
        label_visibility="collapsed",
    )
with button_col:
    load_sample_clicked = st.button("Nạp truy vấn", use_container_width=True)

if load_sample_clicked:
    if selected_sample_label == placeholder_label:
        st.warning("Vui lòng chọn một truy vấn mẫu trước khi bấm \"Nạp truy vấn\".")
    else:
        st.session_state["query_input"] = label_to_query[selected_sample_label]
        st.rerun()

st.caption(
    "Dữ liệu mẫu được trích xuất từ tập kiểm thử độc lập (Independent Test Set) "
    "nhằm đánh giá tính nhất quán của 3 mô hình."
)

st.divider()

if "query_input" not in st.session_state:
    st.session_state["query_input"] = ""

query_input = st.text_area(
    "Nhập câu truy vấn SQL cần kiểm tra:",
    placeholder="Ví dụ: SELECT * FROM users WHERE id = 1",
    height=100,
    key="query_input",
)

check_clicked = st.button("Kiểm tra truy vấn", type="primary")

st.divider()

if check_clicked:
    stripped_input = query_input.strip() if query_input else ""

    if not stripped_input:
        st.warning("Vui lòng nhập câu truy vấn trước khi kiểm tra.")
    elif len(stripped_input) < 4:
        st.warning(
            "Câu truy vấn quá ngắn (dưới 4 ký tự) để mô hình đưa ra dự đoán "
            "đáng tin cậy. Vui lòng nhập câu truy vấn đầy đủ hơn."
        )
    else:
        r_rf = predict_rf(models["tier1_rf"], query_input)
        r_t2 = predict_tier2(models["tier2_model"], query_input)
        r_t3 = predict_tier3(models["tier3_model"], query_input)

        results = {
            "Random Forest (Tầng 1)": r_rf,
            "LSTM baseline (Tầng 2)": r_t2,
            "LSTM+Attention (Tầng 3)": r_t3,
        }

        st.markdown('<div class="soc-section-label">Kết quả kiểm tra</div>', unsafe_allow_html=True)
        st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)

        col_rf, col_t2, col_t3 = st.columns(3)
        columns = [col_rf, col_t2, col_t3]

        for col, (model_name, result) in zip(columns, results.items()):
            is_sqli = result["label"] == 1
            badge_text = "BLOCKED (SQL Injection)" if is_sqli else "CLEAN (Legitimate)"
            badge_class = "model-badge-blocked" if is_sqli else "model-badge-clean"
            confidence_pct = result["prob"] * 100

            with col:
                st.markdown(
                    f"""
                    <div class="model-card">
                        <div class="model-card-name">{model_name}</div>
                        <div class="model-badge {badge_class}">{badge_text}</div>
                        <div class="model-confidence-label">Confidence Score</div>
                        <div class="model-confidence">{confidence_pct:.2f}%</div>
                        <div class="model-latency">Latency: {result['elapsed_ms']:.1f} ms</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if "alpha_weights" in result:
                    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)
                    st.markdown(
                        '<div class="soc-section-caption" style="margin-bottom: 6px;">'
                        "Trọng số attention trên câu truy vấn:</div>",
                        unsafe_allow_html=True,
                    )
                    heatmap_html = render_attention_heatmap_html(
                        result["display_text"], result["alpha_weights"]
                    )
                    st.markdown(heatmap_html, unsafe_allow_html=True)
                    st.markdown(
                        """
                        <div class="attn-legend">
                            <span class="attn-legend-label">Phân tán (Thấp)</span>
                            <div class="attn-legend-bar"></div>
                            <span class="attn-legend-label">Tập trung (Cao)</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        _render_consensus_banner(results)

        st.session_state.setdefault("history", []).append({
            "query": query_input, "results": results, "timestamp": time.time(),
        })

render_session_stats()