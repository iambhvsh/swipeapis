from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import markdown2

from app.finance.router import router as finance_router
from app.search.router import router as search_router
from app.news.router import router as news_router
from app.youtubemusic.router import router as youtubemusic_router

# Disable default docs
app = FastAPI(
    title="Swipe APIs",
    description="A production-ready API hub for Finance, Search, and News.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(finance_router, prefix="/finance", tags=["Finance"])
app.include_router(search_router, prefix="/search", tags=["Search"])
app.include_router(news_router, prefix="/news", tags=["News"])
app.include_router(youtubemusic_router, prefix="/youtubemusic", tags=["YouTube Music"])


@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def read_root_and_serve_docs():
    
    with open("README.md", "r") as f:
        md_content = f.read()

    html_from_markdown = markdown2.markdown(
        md_content,
        extras=[
            "fenced-code-blocks",
            "code-friendly", 
            "tables",
            "break-on-newline",
            "cuddled-lists"
        ]
    )

    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>🚀 Swipe APIs Documentation</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css" media="(prefers-color-scheme: light)">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css" media="(prefers-color-scheme: dark)">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
        <style>
            :root {{
                --color-canvas-default: #ffffff;
                --color-canvas-subtle: #f6f8fa;
                --color-border-default: #d0d7de;
                --color-border-muted: #d8dee4;
                --color-neutral-muted: #656d76;
                --color-fg-default: #1f2328;
                --color-fg-muted: #656d76;
                --color-accent-fg: #0969da;
                --color-success-fg: #1a7f37;
                --color-attention-fg: #9a6700;
                --color-severe-fg: #bc4c00;
                --color-danger-fg: #d1242f;
                --font-stack-default: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
                --font-stack-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
            }}

            * {{
                box-sizing: border-box;
            }}

            body {{
                font-family: var(--font-stack-default);
                font-size: 16px;
                line-height: 1.5;
                color: var(--color-fg-default);
                background-color: var(--color-canvas-default);
                margin: 0;
                padding: 0;
            }}

            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 32px;
            }}

            /* Typography */
            h1 {{
                font-size: 2rem;
                font-weight: 600;
                line-height: 1.25;
                margin: 0 0 16px 0;
                padding-bottom: 10px;
                border-bottom: 1px solid var(--color-border-muted);
                color: var(--color-fg-default);
            }}

            h2 {{
                font-size: 1.5rem;
                font-weight: 600;
                line-height: 1.25;
                margin: 24px 0 16px 0;
                padding-bottom: 8px;
                border-bottom: 1px solid var(--color-border-muted);
                color: var(--color-fg-default);
            }}

            h3 {{
                font-size: 1.25rem;
                font-weight: 600;
                line-height: 1.25;
                margin: 24px 0 16px 0;
                color: var(--color-fg-default);
            }}

            h4 {{
                font-size: 1rem;
                font-weight: 600;
                line-height: 1.25;
                margin: 24px 0 16px 0;
                color: var(--color-fg-default);
            }}

            p {{
                margin: 0 0 16px 0;
            }}

            ul, ol {{
                padding-left: 32px;
                margin: 0 0 16px 0;
            }}

            li {{
                margin: 4px 0;
            }}

            /* Code styling */
            code {{
                font-family: var(--font-stack-mono);
                font-size: 0.85em;
                background-color: rgba(175, 184, 193, 0.2);
                padding: 2px 4px;
                border-radius: 6px;
                color: var(--color-fg-default);
            }}

            pre {{
                font-family: var(--font-stack-mono);
                font-size: 0.85em;
                background-color: var(--color-canvas-subtle);
                border: 1px solid var(--color-border-default);
                border-radius: 6px;
                padding: 16px;
                margin: 0 0 16px 0;
                overflow-x: auto;
                line-height: 1.45;
            }}

            pre code {{
                background: none;
                padding: 0;
                border-radius: 0;
                font-size: inherit;
                color: inherit;
                display: block;
            }}

            /* Tables */
            .table-container {{
                overflow-x: auto;
                margin: 0 0 16px 0;
                border: 1px solid var(--color-border-default);
                border-radius: 6px;
                background: var(--color-canvas-default);
            }}

            table {{
                border-collapse: collapse;
                border-spacing: 0;
                width: 100%;
                min-width: 600px;
            }}

            th, td {{
                padding: 12px 16px;
                text-align: left;
                border-bottom: 1px solid var(--color-border-default);
                white-space: nowrap;
            }}

            th {{
                background-color: var(--color-canvas-subtle);
                font-weight: 600;
                font-size: 0.875rem;
                color: var(--color-fg-muted);
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border-bottom: 2px solid var(--color-border-default);
            }}

            td {{
                font-size: 0.9rem;
            }}

            tr:last-child td {{
                border-bottom: none;
            }}

            tr:hover {{
                background-color: rgba(175, 184, 193, 0.1);
            }}

            /* Links */
            a {{
                color: var(--color-accent-fg);
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}

            /* Blockquotes */
            blockquote {{
                padding: 0 1em;
                color: var(--color-fg-muted);
                border-left: 0.25em solid var(--color-border-default);
                margin: 0 0 16px 0;
            }}

            /* HR */
            hr {{
                height: 0.25em;
                padding: 0;
                margin: 24px 0;
                background-color: var(--color-border-default);
                border: 0;
            }}

            /* Badges/Tags */
            .badge {{
                display: inline-block;
                padding: 2px 6px;
                font-size: 0.75rem;
                font-weight: 500;
                line-height: 1;
                border-radius: 12px;
                background-color: var(--color-neutral-muted);
                color: white;
                margin: 2px;
            }}

            .badge-required {{
                background-color: var(--color-danger-fg);
            }}

            .badge-optional {{
                background-color: var(--color-neutral-muted);
            }}

            /* Parameter styling */
            .param-name {{
                font-family: var(--font-stack-mono);
                font-weight: 600;
                color: var(--color-accent-fg);
            }}

            /* Responsive */
            @media (max-width: 768px) {{
                .container {{
                    padding: 16px;
                }}

                h1 {{
                    font-size: 1.75rem;
                }}

                h2 {{
                    font-size: 1.375rem;
                }}

                pre {{
                    padding: 12px;
                }}
            }}

            /* Dark mode support */
            @media (prefers-color-scheme: dark) {{
                :root {{
                    --color-canvas-default: #000000;
                    --color-canvas-subtle: #161b22;
                    --color-border-default: #30363d;
                    --color-border-muted: #21262d;
                    --color-neutral-muted: #7d8590;
                    --color-fg-default: #e6edf3;
                    --color-fg-muted: #7d8590;
                    --color-accent-fg: #2f81f7;
                    --color-success-fg: #3fb950;
                    --color-attention-fg: #d29922;
                    --color-severe-fg: #db6d28;
                    --color-danger-fg: #f85149;
                }}

                code {{
                    background-color: rgba(110, 118, 129, 0.4);
                }}
            }}

            /* Enhanced styling for API documentation */
            .api-section {{
                margin: 48px 0;
                scroll-margin-top: 80px;
            }}

            .endpoint-badge {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                font-family: var(--font-stack-mono);
                font-size: 0.9rem;
                font-weight: 600;
                color: white;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 8px 16px;
                border-radius: 20px;
                margin: 12px 0;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }}

            .method-get {{
                background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
            }}

            .feature-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 16px;
                margin: 24px 0;
            }}

            .feature-item {{
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 12px 16px;
                background-color: var(--color-canvas-subtle);
                border-radius: 8px;
                border-left: 4px solid var(--color-accent-fg);
                font-size: 0.9rem;
            }}

            .hero-section h1 {{
                color: white;
                border-bottom: none;
                margin-bottom: 16px;
                font-size: 3rem;
            }}

            .hero-section p {{
                font-size: 1.2rem;
                opacity: 0.9;
                max-width: 600px;
                margin: 0 auto 32px auto;
            }}

            .badge-container {{
                display: flex;
                justify-content: center;
                gap: 12px;
                flex-wrap: wrap;
                margin-top: 24px;
            }}

            .status-badge {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 6px 12px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                font-size: 0.8rem;
                font-weight: 500;
                backdrop-filter: blur(10px);
            }}

            .quick-start {{
                background: var(--color-canvas-subtle);
                padding: 24px;
                border-radius: 8px;
                border-left: 4px solid var(--color-success-fg);
                margin: 32px 0;
            }}

            .api-card {{
                background: var(--color-canvas-default);
                border: 1px solid var(--color-border-default);
                border-radius: 12px;
                padding: 32px;
                margin: 32px 0;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                transition: box-shadow 0.2s ease;
            }}

            .api-card:hover {{
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }}

            .parameter-tag {{
                display: inline-block;
                font-family: var(--font-stack-mono);
                font-size: 0.75rem;
                font-weight: 600;
                padding: 2px 6px;
                border-radius: 4px;
                margin-right: 8px;
            }}

            .param-required {{
                background-color: #fef2f2;
                color: #dc2626;
                border: 1px solid #fecaca;
            }}

            .param-optional {{
                background-color: #f3f4f6;
                color: #6b7280;
                border: 1px solid #d1d5db;
            }}

            @media (prefers-color-scheme: dark) {{
                .param-required {{
                    background-color: rgba(239, 68, 68, 0.1);
                    color: #fca5a5;
                    border: 1px solid rgba(239, 68, 68, 0.3);
                }}

                .param-optional {{
                    background-color: rgba(156, 163, 175, 0.1);
                    color: #d1d5db;
                    border: 1px solid rgba(156, 163, 175, 0.3);
                }}

                .feature-item {{
                    background-color: var(--color-canvas-subtle);
                    border-left-color: var(--color-accent-fg);
                }}

                .quick-start {{
                    background: var(--color-canvas-subtle);
                    border-left-color: var(--color-success-fg);
                }}

                .api-card {{
                    background: var(--color-canvas-default);
                    border-color: var(--color-border-default);
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {html_from_markdown}
        </div>
        <script>
            // Wrap tables in scrollable containers
            document.addEventListener('DOMContentLoaded', function() {{
                const tables = document.querySelectorAll('table');
                tables.forEach(function(table) {{
                    if (!table.parentElement.classList.contains('table-container')) {{
                        const wrapper = document.createElement('div');
                        wrapper.className = 'table-container';
                        table.parentNode.insertBefore(wrapper, table);
                        wrapper.appendChild(table);
                    }}
                }});
            }});
            
            // Initialize syntax highlighting
            hljs.highlightAll();
            
            // Add copy buttons to code blocks
            document.addEventListener('DOMContentLoaded', function() {{
                const codeBlocks = document.querySelectorAll('pre code');
                codeBlocks.forEach(function(block) {{
                    const button = document.createElement('button');
                    button.innerText = 'Copy';
                    button.style.cssText = `
                        position: absolute;
                        top: 8px;
                        right: 8px;
                        background: var(--color-neutral-muted);
                        color: white;
                        border: none;
                        padding: 4px 8px;
                        border-radius: 4px;
                        font-size: 0.75rem;
                        cursor: pointer;
                        opacity: 0;
                        transition: opacity 0.2s;
                    `;
                    
                    const pre = block.parentElement;
                    pre.style.position = 'relative';
                    pre.appendChild(button);
                    
                    pre.addEventListener('mouseenter', function() {{
                        button.style.opacity = '1';
                    }});
                    
                    pre.addEventListener('mouseleave', function() {{
                        button.style.opacity = '0';
                    }});
                    
                    button.addEventListener('click', function() {{
                        navigator.clipboard.writeText(block.textContent);
                        button.innerText = 'Copied!';
                        setTimeout(() => {{
                            button.innerText = 'Copy';
                        }}, 2000);
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=full_html)
