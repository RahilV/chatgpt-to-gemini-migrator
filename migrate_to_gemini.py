import json
import os
import sys
from datetime import datetime
from pathlib import Path
import html
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

class ChatGPTMigrator:
    """Migrates ChatGPT conversations to various formats for Gemini compatibility."""
    
    def __init__(self, conversations_file=None):
        # Check for file in input folder first, then root
        if conversations_file is None:
            if Path('input/conversations.json').exists():
                conversations_file = 'input/conversations.json'
            elif Path('conversations.json').exists():
                conversations_file = 'conversations.json'
            else:
                conversations_file = 'input/conversations.json'  # Default location
        
        self.conversations_file = conversations_file
        self.conversations = []
        self.output_dir = Path('migrated_conversations')
        
    def load_conversations(self):
        """Load conversations from ChatGPT export."""
        print(f"📂 Loading {self.conversations_file}...")
        
        if not Path(self.conversations_file).exists():
            print(f"❌ Error: {self.conversations_file} not found!")
            print(f"\\n💡 Please place your conversations.json file in the 'input' folder")
            print(f"   Expected location: {Path('input/conversations.json').absolute()}")
            raise FileNotFoundError(f"{self.conversations_file} not found")
        
        with open(self.conversations_file, 'r', encoding='utf-8') as f:
            self.conversations = json.load(f)
        print(f"✅ Loaded {len(self.conversations)} conversations")
        
    def extract_conversation_data(self, conv):
        """Extract structured data from a single conversation."""
        title = conv.get('title', 'Untitled Conversation')
        create_time = conv.get('create_time')
        update_time = conv.get('update_time')
        
        # Extract messages from mapping
        messages = []
        mapping = conv.get('mapping', {})
        
        # Build message tree
        for node_id, node_data in mapping.items():
            message = node_data.get('message')
            if message and message.get('content'):
                content = message.get('content', {})
                author = message.get('author', {})
                role = author.get('role', 'unknown')
                
                # Extract text content
                parts = content.get('parts', [])
                text_content = []
                for part in parts:
                    if isinstance(part, str):
                        text_content.append(part)
                    elif isinstance(part, dict):
                        # Handle complex content types
                        text_content.append(str(part))
                
                if text_content:
                    messages.append({
                        'role': role,
                        'content': '\n'.join(text_content),
                        'create_time': message.get('create_time'),
                        'id': message.get('id')
                    })
        
        # Sort messages by creation time (handle None values)
        messages.sort(key=lambda x: x.get('create_time') or 0)
        
        return {
            'title': title,
            'create_time': create_time,
            'update_time': update_time,
            'create_date': datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S') if create_time else 'Unknown',
            'messages': messages,
            'message_count': len(messages)
        }
    
    def export_to_markdown(self):
        """Export each conversation as a markdown file."""
        md_dir = self.output_dir / 'markdown'
        md_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📝 Exporting to Markdown...")
        
        for idx, conv in enumerate(self.conversations, 1):
            data = self.extract_conversation_data(conv)
            
            # Create safe filename
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', data['title'])[:100]
            filename = f"{idx:04d}_{safe_title}.md"
            
            # Generate markdown content
            md_content = f"# {data['title']}\n\n"
            md_content += f"**Created:** {data['create_date']}  \n"
            md_content += f"**Messages:** {data['message_count']}\n\n"
            md_content += "---\n\n"
            
            for msg in data['messages']:
                role = msg['role'].upper()
                content = msg['content']
                timestamp = datetime.fromtimestamp(msg['create_time']).strftime('%Y-%m-%d %H:%M:%S') if msg.get('create_time') else ''
                
                if role == 'USER':
                    md_content += f"## 👤 User\n"
                elif role == 'ASSISTANT':
                    md_content += f"## 🤖 Assistant\n"
                else:
                    md_content += f"## {role}\n"
                
                if timestamp:
                    md_content += f"*{timestamp}*\n\n"
                
                md_content += f"{content}\n\n"
                md_content += "---\n\n"
            
            # Write file
            with open(md_dir / filename, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            if idx % 50 == 0:
                print(f"  Processed {idx}/{len(self.conversations)} conversations...")
        
        print(f"✅ Exported {len(self.conversations)} markdown files to {md_dir}")
    
    def export_to_json(self):
        """Export conversations to a clean JSON format."""
        json_dir = self.output_dir / 'json'
        json_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📦 Exporting to JSON...")
        
        all_conversations = []
        for conv in self.conversations:
            data = self.extract_conversation_data(conv)
            all_conversations.append(data)
        
        # Single file with all conversations
        output_file = json_dir / 'all_conversations.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_conversations, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exported to {output_file}")
    
    def export_to_csv(self):
        """Export conversation metadata to CSV for analysis."""
        import csv
        
        csv_dir = self.output_dir / 'csv'
        csv_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📊 Exporting to CSV...")
        
        # Conversation summary CSV
        with open(csv_dir / 'conversation_summary.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Title', 'Created', 'Updated', 'Message Count', 'User Messages', 'Assistant Messages'])
            
            for idx, conv in enumerate(self.conversations, 1):
                data = self.extract_conversation_data(conv)
                user_count = sum(1 for m in data['messages'] if m['role'] == 'user')
                assistant_count = sum(1 for m in data['messages'] if m['role'] == 'assistant')
                
                writer.writerow([
                    idx,
                    data['title'],
                    data['create_date'],
                    datetime.fromtimestamp(data['update_time']).strftime('%Y-%m-%d %H:%M:%S') if data['update_time'] else '',
                    data['message_count'],
                    user_count,
                    assistant_count
                ])
        
        print(f"✅ Exported to {csv_dir / 'conversation_summary.csv'}")
    
    def generate_html_viewer(self):
        """Generate an interactive HTML viewer for all conversations."""
        html_dir = self.output_dir / 'html'
        html_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n🌐 Generating HTML viewer...")
        
        # Extract all conversation data
        all_data = []
        for idx, conv in enumerate(self.conversations, 1):
            data = self.extract_conversation_data(conv)
            data['id'] = idx
            all_data.append(data)
        
        # Generate HTML
        html_content = self._generate_html_template(all_data)
        
        output_file = html_dir / 'conversation_viewer.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Generated HTML viewer at {output_file}")
        print(f"   Open this file in your browser to view all conversations!")
    
    def _generate_html_template(self, conversations_data):
        """Generate the HTML template with embedded data."""
        conversations_json = json.dumps(conversations_data, ensure_ascii=False)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatGPT Conversations Viewer</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
            display: grid;
            grid-template-columns: 350px 1fr;
            height: calc(100vh - 40px);
        }}
        
        .sidebar {{
            background: #f8f9fa;
            border-right: 1px solid #e0e0e0;
            display: flex;
            flex-direction: column;
        }}
        
        .header {{
            padding: 30px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .header h1 {{
            font-size: 24px;
            margin-bottom: 10px;
        }}
        
        .stats {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .search-box {{
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .search-box input {{
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            transition: all 0.3s;
        }}
        
        .search-box input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .conversation-list {{
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }}
        
        .conversation-item {{
            padding: 15px;
            margin-bottom: 8px;
            background: white;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
            border: 2px solid transparent;
        }}
        
        .conversation-item:hover {{
            background: #f0f0f0;
            transform: translateX(5px);
        }}
        
        .conversation-item.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}
        
        .conversation-item .title {{
            font-weight: 600;
            margin-bottom: 5px;
            font-size: 14px;
        }}
        
        .conversation-item .meta {{
            font-size: 12px;
            opacity: 0.7;
        }}
        
        .main-content {{
            display: flex;
            flex-direction: column;
            background: white;
        }}
        
        .content-header {{
            padding: 30px;
            border-bottom: 1px solid #e0e0e0;
            background: #fafafa;
        }}
        
        .content-header h2 {{
            font-size: 28px;
            margin-bottom: 10px;
            color: #333;
        }}
        
        .content-header .info {{
            color: #666;
            font-size: 14px;
        }}
        
        .messages {{
            flex: 1;
            overflow-y: auto;
            padding: 30px;
        }}
        
        .message {{
            margin-bottom: 30px;
            animation: fadeIn 0.3s;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .message-header {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            gap: 10px;
        }}
        
        .message-role {{
            font-weight: 700;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .message.user .message-role {{
            color: #667eea;
        }}
        
        .message.assistant .message-role {{
            color: #764ba2;
        }}
        
        .message-time {{
            font-size: 12px;
            color: #999;
        }}
        
        .message-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 12px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        
        .message.user .message-content {{
            background: #e7f3ff;
            border-left: 4px solid #667eea;
        }}
        
        .message.assistant .message-content {{
            background: #f3e7ff;
            border-left: 4px solid #764ba2;
        }}
        
        .empty-state {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #999;
            font-size: 18px;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #999;
        }}
        
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #f1f1f1;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: #888;
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #555;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="header">
                <h1>💬 ChatGPT Archive</h1>
                <div class="stats">
                    <div id="totalConversations"></div>
                    <div id="totalMessages"></div>
                </div>
            </div>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Search conversations...">
            </div>
            <div class="conversation-list" id="conversationList"></div>
        </div>
        
        <div class="main-content">
            <div class="content-header" id="contentHeader" style="display: none;">
                <h2 id="conversationTitle"></h2>
                <div class="info" id="conversationInfo"></div>
            </div>
            <div class="messages" id="messagesContainer">
                <div class="empty-state">
                    👈 Select a conversation to view
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const conversations = {conversations_json};
        let filteredConversations = conversations;
        let currentConversation = null;
        
        function init() {{
            updateStats();
            renderConversationList();
            setupSearch();
        }}
        
        function updateStats() {{
            const totalMessages = conversations.reduce((sum, conv) => sum + conv.message_count, 0);
            document.getElementById('totalConversations').textContent = `${{conversations.length}} conversations`;
            document.getElementById('totalMessages').textContent = `${{totalMessages}} messages`;
        }}
        
        function renderConversationList() {{
            const listEl = document.getElementById('conversationList');
            
            if (filteredConversations.length === 0) {{
                listEl.innerHTML = '<div class="no-results">No conversations found</div>';
                return;
            }}
            
            listEl.innerHTML = filteredConversations.map(conv => `
                <div class="conversation-item" onclick="selectConversation(${{conv.id}})" id="conv-${{conv.id}}">
                    <div class="title">${{escapeHtml(conv.title)}}</div>
                    <div class="meta">${{conv.create_date}} • ${{conv.message_count}} messages</div>
                </div>
            `).join('');
        }}
        
        function selectConversation(id) {{
            currentConversation = conversations.find(c => c.id === id);
            
            // Update active state
            document.querySelectorAll('.conversation-item').forEach(el => el.classList.remove('active'));
            document.getElementById(`conv-${{id}}`).classList.add('active');
            
            // Render conversation
            renderConversation();
        }}
        
        function renderConversation() {{
            if (!currentConversation) return;
            
            // Update header
            document.getElementById('contentHeader').style.display = 'block';
            document.getElementById('conversationTitle').textContent = currentConversation.title;
            document.getElementById('conversationInfo').textContent = 
                `Created: ${{currentConversation.create_date}} • ${{currentConversation.message_count}} messages`;
            
            // Render messages
            const messagesEl = document.getElementById('messagesContainer');
            messagesEl.innerHTML = currentConversation.messages.map(msg => {{
                const time = msg.create_time ? new Date(msg.create_time * 1000).toLocaleString() : '';
                return `
                    <div class="message ${{msg.role}}">
                        <div class="message-header">
                            <span class="message-role">${{msg.role === 'user' ? '👤 User' : '🤖 Assistant'}}</span>
                            <span class="message-time">${{time}}</span>
                        </div>
                        <div class="message-content">${{escapeHtml(msg.content)}}</div>
                    </div>
                `;
            }}).join('');
            
            messagesEl.scrollTop = 0;
        }}
        
        function setupSearch() {{
            const searchInput = document.getElementById('searchInput');
            searchInput.addEventListener('input', (e) => {{
                const query = e.target.value.toLowerCase();
                
                if (!query) {{
                    filteredConversations = conversations;
                }} else {{
                    filteredConversations = conversations.filter(conv => 
                        conv.title.toLowerCase().includes(query) ||
                        conv.messages.some(msg => msg.content.toLowerCase().includes(query))
                    );
                }}
                
                renderConversationList();
            }});
        }}
        
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        init();
    </script>
</body>
</html>"""
    
    def run_migration(self):
        """Run the complete migration process."""
        print("🚀 Starting ChatGPT to Gemini Migration\n")
        print("=" * 60)
        
        self.load_conversations()
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Run all exports
        self.export_to_markdown()
        self.export_to_json()
        self.export_to_csv()
        self.generate_html_viewer()
        
        print("\n" + "=" * 60)
        print("✨ Migration Complete!")
        print(f"\n📁 All files saved to: {self.output_dir.absolute()}")
        print("\n📋 What was created:")
        print(f"  • {len(self.conversations)} Markdown files (markdown/)")
        print(f"  • 1 JSON file with all conversations (json/)")
        print(f"  • 1 CSV summary file (csv/)")
        print(f"  • 1 Interactive HTML viewer (html/)")
        print("\n💡 Next steps:")
        print("  1. Open html/conversation_viewer.html in your browser")
        print("  2. Browse your conversations and copy relevant ones")
        print("  3. Paste into new Gemini conversations as needed")
        print("  4. Use markdown files for easy reference")

def main():
    migrator = ChatGPTMigrator()
    migrator.run_migration()

if __name__ == "__main__":
    main()
