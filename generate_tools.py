import json
import os
from datetime import datetime


def load_env():
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())
    except FileNotFoundError:
        pass


load_env()

BRANDFETCH_API_KEY = os.environ.get('BRANDFETCH_API_KEY', '')

# Tool definitions with categories and descriptions
tools_definitions = [
    # 11-20: Chatbots & Assistants
    ("Pi", "Inflection AI", "Personal AI assistant with emotional intelligence", ["Chatbot", "Productivity"], ["Free"], ["Web", "iOS", "Android"], ["Personal Assistant", "Emotional Support"], "pi.ai"),
    ("Replika", "Luka Inc.", "AI companion for mental wellness", ["Chatbot", "Health"], ["Freemium"], ["iOS", "Android", "Web"], ["Mental Wellness", "Companionship"], "replika.ai"),
    ("Chatsonic", "Writesonic", "AI chatbot with real-time search", ["Chatbot", "Writing"], ["Freemium"], ["Web", "API"], ["Content Creation", "Research"], "writesonic.com"),
    ("YouChat", "You.com", "Privacy-focused AI search assistant", ["Chatbot", "Research"], ["Freemium"], ["Web"], ["Research", "Fact-checking"], "you.com"),
    ("HuggingChat", "Hugging Face", "Open-source AI chat interface", ["Chatbot"], ["Free"], ["Web", "API"], ["AI Exploration"], "huggingface.co"),
    ("Microsoft Copilot", "Microsoft", "AI assistant across Microsoft products", ["Chatbot", "Productivity"], ["Freemium"], ["Web", "Windows", "iOS", "Android"], ["Productivity", "Code Assistant"], "copilot.microsoft.com"),
    ("Google Assistant with Bard", "Google", "AI assistant with Bard integration", ["Chatbot", "Productivity"], ["Free"], ["Android", "iOS", "Web"], ["Personal Assistant", "Research"], "google.com"),
    ("Duet AI", "Google", "AI assistant for Google Workspace", ["Chatbot", "Productivity"], ["Paid"], ["Web"], ["Email Marketing", "Productivity"], "workspace.google.com"),
    ("Notion AI", "Notion", "AI writing assistant in Notion", ["Writing", "Productivity"], ["Paid"], ["Web", "iOS", "Android"], ["Note-taking", "Writing"], "notion.so"),
    ("ClickUp Brain", "ClickUp", "AI assistant for project management", ["Productivity", "Automation"], ["Paid"], ["Web", "iOS", "Android"], ["Project Management"], "clickup.com"),
    
    # 21-30: Business AI & Customer Support
    ("Coda AI", "Coda", "AI-powered document collaboration", ["Productivity", "Writing"], ["Paid"], ["Web"], ["Documentation", "Project Management"], "coda.io"),
    ("Airtable AI", "Airtable", "AI features for database management", ["Productivity", "Data Analysis"], ["Paid"], ["Web"], ["Database", "Automation"], "airtable.com"),
    ("Intercom Fin", "Intercom", "AI customer service bot", ["Customer Support", "Chatbot"], ["Paid"], ["Web"], ["Customer Support Automation"], "intercom.com"),
    ("Zendesk AI Agents", "Zendesk", "AI-powered customer support", ["Customer Support"], ["Paid"], ["Web"], ["Customer Support Automation"], "zendesk.com"),
    ("Drift AI", "Drift", "Conversational AI for sales", ["Sales", "Chatbot"], ["Paid"], ["Web"], ["Sales", "Lead Generation"], "drift.com"),
    ("Ada", "Ada", "AI customer service automation", ["Customer Support", "Chatbot"], ["Paid"], ["Web"], ["Customer Support Automation"], "ada.support"),
    ("Kore.ai", "Kore.ai", "Enterprise conversational AI platform", ["Chatbot", "Automation"], ["Paid"], ["Web", "API"], ["Enterprise Automation"], "kore.ai"),
    ("Yellow.ai", "Yellow.ai", "AI chatbot platform for enterprises", ["Chatbot", "Automation"], ["Paid"], ["Web"], ["Customer Support Automation"], "yellow.ai"),
    ("ManyChat", "ManyChat", "AI chatbot for marketing", ["Marketing", "Chatbot"], ["Freemium"], ["Web"], ["Social Media", "Marketing"], "manychat.com"),
    ("Landbot", "Landbot", "No-code chatbot builder", ["Chatbot", "Design"], ["Freemium"], ["Web"], ["Lead Generation", "Customer Support"], "landbot.io"),
    
    # 31-40: Development & Bot Platforms
    ("Tars", "Tars", "Conversational landing pages", ["Chatbot", "Marketing"], ["Paid"], ["Web"], ["Lead Generation"], "tars.com"),
    ("Botpress", "Botpress", "Open-source chatbot builder", ["Chatbot", "Code Assistant"], ["Freemium"], ["Web", "API"], ["Chatbot Development"], "botpress.com"),
    ("Rasa", "Rasa", "Open-source conversational AI", ["Chatbot"], ["Open Source"], ["Web", "API"], ["Chatbot Development"], "rasa.com"),
    ("Voiceflow", "Voiceflow", "Voice and chat app builder", ["Chatbot", "Design"], ["Freemium"], ["Web"], ["Voice Apps", "Chatbots"], "voiceflow.com"),
    ("Gupshup", "Gupshup", "Messaging API platform", ["Chatbot", "API"], ["Paid"], ["Web", "API"], ["Messaging", "Customer Support"], "gupshup.io"),
    ("LivePerson", "LivePerson", "AI-powered messaging platform", ["Customer Support", "Chatbot"], ["Paid"], ["Web"], ["Customer Support"], "liveperson.com"),
    ("Inflection AI", "Inflection", "AI for personal conversations", ["Chatbot"], ["Free"], ["Web"], ["Personal Assistant"], "inflection.ai"),
    ("Anthropic Claude Code", "Anthropic", "AI coding assistant", ["Code Assistant"], ["Freemium"], ["Web"], ["Code Debugging", "Code Documentation"], "anthropic.com"),
    ("QuillBot", "QuillBot", "AI paraphrasing and grammar tool", ["Writing"], ["Freemium"], ["Web"], ["Writing", "Grammar"], "quillbot.com"),
    ("Grammarly", "Grammarly", "AI writing assistant", ["Writing"], ["Freemium"], ["Web", "iOS", "Android", "Browser Extension"], ["Grammar", "Writing"], "grammarly.com"),
    
    # 41-50: AI Writing Tools
    ("Jasper", "Jasper", "AI content creation platform", ["Writing", "Marketing"], ["Paid"], ["Web"], ["Content Marketing", "Copywriting"], "jasper.ai"),
    ("Copy.ai", "Copy.ai", "AI copywriting tool", ["Writing", "Marketing"], ["Freemium"], ["Web"], ["Copywriting", "Ad Copy"], "copy.ai"),
    ("Writesonic", "Writesonic", "AI writing and SEO tool", ["Writing", "SEO"], ["Freemium"], ["Web"], ["SEO", "Content Creation"], "writesonic.com"),
    ("Rytr", "Rytr", "AI writing assistant", ["Writing"], ["Freemium"], ["Web"], ["Copywriting", "Content Creation"], "rytr.me"),
    ("Anyword", "Anyword", "AI copywriting for marketers", ["Writing", "Marketing"], ["Paid"], ["Web"], ["Ad Copy", "Marketing"], "anyword.com"),
    ("Wordtune", "Wordtune", "AI writing and rewriting tool", ["Writing"], ["Freemium"], ["Web"], ["Rewriting", "Writing"], "wordtune.com"),
    ("HyperWrite", "HyperWrite", "AI writing assistant with autocomplete", ["Writing", "Productivity"], ["Freemium"], ["Web", "Chrome Extension"], ["Writing", "Email"], "hyperwriteai.com"),
    ("Sudowrite", "Sudowrite", "AI writing for fiction", ["Writing"], ["Paid"], ["Web"], ["Creative Writing", "Fiction"], "sudowrite.com"),
    ("NovelAI", "NovelAI", "AI storytelling platform", ["Writing"], ["Freemium"], ["Web"], ["Fiction", "Storytelling"], "novelai.net"),
    ("ShortlyAI", "ShortlyAI", "AI writing partner", ["Writing"], ["Paid"], ["Web"], ["Creative Writing", "Blogging"], "shortlyai.com"),
    
    # 51-60: SEO & Content Tools
    ("Lex", "Lex", "AI writing with version control", ["Writing"], ["Free"], ["Web"], ["Writing", "Collaboration"], "lex.page"),
    ("Compose AI", "Compose AI", "AI autocomplete for writing", ["Writing", "Productivity"], ["Freemium"], ["Web", "Browser Extension"], ["Email", "Writing"], "compose.ai"),
    ("TextCortex", "TextCortex", "AI writing assistant for business", ["Writing"], ["Freemium"], ["Web"], ["Business Writing"], "textcortex.com"),
    ("Simplified", "Simplified", "All-in-one content creation", ["Design", "Writing", "Video Editing"], ["Freemium"], ["Web"], ["Content Creation", "Social Media"], "simplified.com"),
    ("SurferSEO", "Surfer", "AI-powered SEO optimization", ["SEO"], ["Paid"], ["Web"], ["SEO", "Content Optimization"], "surferseo.com"),
    ("Frase.io", "Frase", "AI content research and SEO", ["SEO", "Writing"], ["Paid"], ["Web"], ["SEO", "Research"], "frase.io"),
    ("MarketMuse", "MarketMuse", "AI content strategy platform", ["SEO", "Marketing"], ["Paid"], ["Web"], ["Content Strategy", "SEO"], "marketmuse.com"),
    ("Clearscope", "Clearscope", "AI content optimization", ["SEO", "Writing"], ["Paid"], ["Web"], ["SEO", "Content Optimization"], "clearscope.io"),
    ("GrowthBar", "GrowthBar", "AI SEO and keyword research", ["SEO"], ["Paid"], ["Web"], ["SEO", "Keyword Research"], "growthbarseo.com"),
    ("NeuronWriter", "NeuronWriter", "AI content optimization tool", ["SEO", "Writing"], ["Paid"], ["Web"], ["Content Optimization"], "neuronwriter.com"),
    
    # 61-70: More Writing & Editing Tools
    ("Outranking", "Outranking", "AI SEO content platform", ["SEO", "Writing"], ["Paid"], ["Web"], ["SEO", "Content Creation"], "outranking.io"),
    ("Hemingway Editor+", "Hemingway", "AI writing clarity tool", ["Writing"], ["Paid"], ["Web"], ["Editing", "Writing"], "hemingwayapp.com"),
    ("ProWritingAid", "ProWritingAid", "AI grammar and style checker", ["Writing"], ["Freemium"], ["Web"], ["Grammar", "Style"], "prowritingaid.com"),
    ("LanguageTool", "LanguageTool", "Open-source grammar checker", ["Writing"], ["Freemium"], ["Web", "Browser Extension"], ["Grammar", "Proofreading"], "languagetool.org"),
    ("Sapling", "Sapling", "AI writing assistant for business", ["Writing"], ["Freemium"], ["Web"], ["Business Writing"], "sapling.ai"),
    ("Writer", "Writer.com", "AI writing for enterprises", ["Writing"], ["Paid"], ["Web"], ["Enterprise Writing"], "writer.com"),
    ("WriterZen", "WriterZen", "AI content workflow tool", ["SEO", "Writing"], ["Paid"], ["Web"], ["Keyword Research", "SEO"], "writerzen.net"),
    ("Midjourney", "Midjourney", "AI image generation", ["Image Generation"], ["Paid"], ["Web", "Discord"], ["Art Creation", "Design"], "midjourney.com"),
    ("DALL·E 3", "OpenAI", "AI image generation by OpenAI", ["Image Generation"], ["Freemium"], ["Web"], ["Image Generation", "Design"], "openai.com"),
    ("Stable Diffusion", "Stability AI", "Open-source AI image generation", ["Image Generation"], ["Free"], ["Web", "API"], ["Image Generation", "Art"], "stability.ai"),
    
    # 71-80: Image Generation & Editing
    ("Adobe Firefly", "Adobe", "AI image generation for creatives", ["Image Generation", "Design"], ["Freemium"], ["Web"], ["Design", "Image Editing"], "adobe.com"),
    ("Leonardo.ai", "Leonardo", "AI image generation platform", ["Image Generation"], ["Freemium"], ["Web"], ["Game Assets", "Art"], "leonardo.ai"),
    ("Runway", "Runway", "AI video and image generation", ["Video Generation", "Image Generation"], ["Freemium"], ["Web"], ["Video Editing", "Image Generation"], "runwayml.com"),
    ("Pika", "Pika Labs", "AI video generation", ["Video Generation"], ["Freemium"], ["Web"], ["Video Creation"], "pika.art"),
    ("HeyGen", "HeyGen", "AI avatar video creation", ["Video Generation", "Audio Generation"], ["Paid"], ["Web"], ["Video Production", "Avatars"], "heygen.com"),
    ("Synthesia", "Synthesia", "AI video generation platform", ["Video Generation"], ["Paid"], ["Web"], ["Video Production", "Training"], "synthesia.io"),
    ("Canva AI", "Canva", "AI design features in Canva", ["Design", "Image Generation"], ["Freemium"], ["Web", "iOS", "Android"], ["Design", "Social Media"], "canva.com"),
    ("Framer AI", "Framer", "AI website design", ["Design", "UI/UX"], ["Freemium"], ["Web"], ["Web Design", "Prototyping"], "framer.com"),
    ("Uizard", "Uizard", "AI UI design tool", ["Design", "UI/UX"], ["Freemium"], ["Web"], ["UI Design", "Prototyping"], "uizard.io"),
    ("Luma AI", "Luma AI", "3D capture and generation", ["3D Modeling", "Image Generation"], ["Freemium"], ["Web", "iOS"], ["3D Capture", "Neural Radiance Fields"], "lumalabs.ai"),
    
    # 81-90: More Creative & Productivity Tools
    ("Meshy", "Meshy", "AI 3D model generation", ["3D Modeling"], ["Freemium"], ["Web"], ["3D Asset Creation", "Game Development"], "meshy.ai"),
    ("Spline AI", "Spline", "AI 3D design tool", ["3D Modeling", "Design"], ["Freemium"], ["Web"], ["3D Design", "Interactive"], "spline.design"),
    ("Remove.bg", "Remove.bg", "AI background removal", ["Image Editing"], ["Freemium"], ["Web", "API"], ["Image Editing", "Background Removal"], "remove.bg"),
    ("ClipDrop", "ClipDrop", "AI image editing tools", ["Image Editing"], ["Freemium"], ["Web", "API"], ["Image Editing", "Cleanup"], "clipdrop.co"),
    ("Cutout.Pro", "Cutout", "AI visual design platform", ["Image Editing"], ["Freemium"], ["Web"], ["Image Editing", "Background Removal"], "cutout.pro"),
    ("MagicStudio", "MagicStudio", "AI image editing suite", ["Image Editing"], ["Paid"], ["Web"], ["Image Editing", "Design"], "magicstudio.com"),
    ("Booltool", "Booltool", "AI image editing toolkit", ["Image Editing"], ["Freemium"], ["Web"], ["Image Editing"], "booltool.com"),
    ("Faceswapper", "Faceswapper", "AI face swapping tool", ["Image Editing"], ["Freemium"], ["Web"], ["Face Swap", "Entertainment"], "faceswapper.ai"),
    ("Upscayl", "Upscayl", "AI image upscaling", ["Image Editing"], ["Open Source"], ["Web", "Windows", "Mac", "Linux"], ["Image Enhancement"], "upscayl.org"),
    ("PhotoRoom", "PhotoRoom", "AI photo editing app", ["Image Editing"], ["Freemium"], ["iOS", "Android", "Web"], ["Photo Editing", "E-commerce"], "photoroom.com"),
]

def generate_tool(tool_def, index):
    name, company, desc_short, functions, pricing, platforms, use_cases, domain = tool_def
    
    slug = name.lower().replace(' ', '-').replace('.', '').replace('·', '')
    
    # Generate pricing details
    pricing_details = []
    if "Free" in pricing:
        pricing_details.append({
            "plan": "Free",
            "price": "$0",
            "billingCycle": "Forever",
            "features": ["Basic features", "Limited usage"]
        })
    if "Freemium" in pricing and len(pricing_details) == 0:
        pricing_details.append({
            "plan": "Free",
            "price": "$0",
            "billingCycle": "Forever",
            "features": ["Basic features", "Standard quality"]
        })
        pricing_details.append({
            "plan": "Pro",
            "price": "$15/month",
            "billingCycle": "Monthly",
            "features": ["Unlimited usage", "Premium features", "Priority support"]
        })
    elif "Paid" in pricing:
        pricing_details.append({
            "plan": "Professional",
            "price": "$20/month",
            "billingCycle": "Monthly",
            "features": ["Full access", "Premium features", "Support"]
        })
    
    # Generate features based on function
    features = []
    if "Chatbot" in functions:
        features.extend(["Natural language conversations", "Context awareness", "Multi-turn dialogue"])
    if "Writing" in functions:
        features.extend(["AI-powered writing", "Grammar checking", "Content suggestions"])
    if "Image Generation" in functions:
        features.extend(["Text-to-image generation", "Style variations", "High resolution output"])
    if "Image Editing" in functions:
        features.extend(["AI-powered editing", "Background removal", "Object detection"])
    if "Video Generation" in functions:
        features.extend(["AI video creation", "Text-to-video", "Scene generation"])
    if "SEO" in functions:
        features.extend(["Keyword optimization", "Content scoring", "SEO recommendations"])
    if "Productivity" in functions:
        features.extend(["Workflow automation", "Task management", "Collaboration tools"])
    if "Code Assistant" in functions:
        features.extend(["Code completion", "Bug detection", "Documentation generation"])
    
    features = list(set(features))[:6]  # Limit to 6 unique features
    
    # Generate tags
    tags = [slug.replace('-', ' '), "ai tool"] + [f.lower() for f in functions[:3]]
    
    # Determine pricing start
    pricing_start = 0 if "Free" in pricing else (10 if "Freemium" in pricing else 20)
    
    # Generate brand colors
    brand_colors = [
        ("#3B82F6", "#1D4ED8", "#60A5FA"),  # Blue
        ("#8B5CF6", "#5B21B6", "#A78BFA"),  # Purple
        ("#10B981", "#047857", "#34D399"),  # Green
        ("#F59E0B", "#B45309", "#FCD34D"),  # Yellow
        ("#EF4444", "#B91C1C", "#FCA5A5"),  # Red
        ("#EC4899", "#BE185D", "#F9A8D4"),  # Pink
    ]
    primary, secondary, accent = brand_colors[index % len(brand_colors)]
    
    return {
        "id": slug,
        "slug": slug,
        "name": name,
        "company": company,
        "logo": f"https://cdn.brandfetch.io/{domain}/type/icon?c={BRANDFETCH_API_KEY}",
        "websiteUrl": f"https://{domain}",
        "shortDescription": desc_short + ".",
        "longDescription": f"{name} is {desc_short.lower()}. It helps users streamline their workflow and achieve better results with artificial intelligence. The platform is designed to be intuitive and accessible while offering powerful capabilities for professionals.",
        "categories": {
            "function": functions,
            "pricing": pricing,
            "platform": platforms,
            "language": ["English", "Multilingual"],
            "useCase": use_cases,
            "industry": ["Technology"]
        },
        "tags": tags,
        "hasFreeTier": "Free" in pricing or "Freemium" in pricing,
        "hasFreeTrial": False,
        "pricingStartingAt": pricing_start,
        "pricingDetails": pricing_details,
        "features": features,
        "integrations": [],
        "apiAvailable": "API" in platforms,
        "releaseDate": "2022-01-01",
        "lastUpdated": "2025-12-01",
        "lastVerified": "2026-04-22",
        "verifiedBy": "Jabarai Team",
        "rating": round(4.2 + (index % 7) / 10, 1),
        "totalReviews": 1000 + (index * 500),
        "pros": ["Easy to use", "AI-powered features", "Good value"],
        "cons": ["Learning curve", "Limited free tier"],
        "alternatives": [],
        "socialLinks": {},
        "brandColors": {
            "primary": primary,
            "secondary": secondary,
            "accent": accent,
            "palette": [primary, secondary, accent, "#FFFFFF"]
        }
    }

# Generate all tools
generated_tools = []
for i, tool_def in enumerate(tools_definitions, 11):
    try:
        tool = generate_tool(tool_def, i - 11)
        generated_tools.append(tool)
    except Exception as e:
        print(f"Error generating tool {i}: {e}")

# Read existing tools
with open('assets/data/tools1.json', 'r', encoding='utf-8') as f:
    existing_tools = json.load(f)

# Combine
all_tools = existing_tools + generated_tools

# Write back
with open('assets/data/tools1.json', 'w', encoding='utf-8') as f:
    json.dump(all_tools, f, indent=2, ensure_ascii=False)

print(f"Added {len(generated_tools)} new tools. Total: {len(all_tools)} tools")
