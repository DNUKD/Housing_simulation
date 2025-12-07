def tooltip_css():
    return """
    <style>

    .tooltip .tooltiptext {
        visibility: hidden;
        opacity: 0;
        transition: opacity 0.25s ease;
    
        position: absolute;
        z-index: 9999;
    
        /* SIZE */
        max-width: 550;
        padding: 16px 14px;
    
        /* DESIGN */
        background-color: #212836;
        color: #fff;
        border-radius: 2px;
    
        top: -20%;
        left: 115%;
        transform: translateY(-50%);
    
        white-space: pre-line;
        overflow-wrap: break-word;
        
        font-size: 13px;
        line-height: 1.4;   
    }
        
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }

    @media (max-width: 2000px) {
        .tooltip .tooltiptext {
            left: 0;
            right: auto;
            transform: none;
        }
    }

    .limited-width-container {
        max-width: 1600px;
        margin-left: auto;
        margin-right: auto;
    }

    .block-container {
        padding-left: 140px !important;
        padding-right: 40px !important;
        padding-top: 20px !important;
    }

    h4 {
        margin-top: 0px !important;
    }

        /* ----------- SECTION TITLE ----------- */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    /* ----------- METRIC LABEL ----------- */
    .metric-label {
        color: #999;
        font-size: 15px;
        display: flex;
        gap: 6px;
        align-items: center;
        margin-bottom: 4px;
    }
    
    /* ----------- METRIC VALUE ----------- */
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #fff;
        margin-bottom: 14px;
    }
    
    /* ----------- METRIC VALUE (COLORED) ----------- */
    .metric-value-colored {
        font-size: 26px;
        font-weight: 700;
    }
    
    /* ----------- WARNING TEXT ----------- */
    .metric-warning {
    font-size: 14px;
    margin-top: -14px;      
    margin-bottom: 0px;    
    }

    
    /* ----------- BLOCK WRAPPER ----------- */
    .metric-block {
        margin-bottom: 14px;
    }
    
    .price-delta {
    color: #5cb85c;
    font-size: 20px;
    margin-left: 6px;
    }


    </style>
    """
