#!/usr/bin/env python3
"""
Data scraper for collecting additional Siemens PLC resources from free sources
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from typing import List, Dict, Any
import re
from urllib.parse import urljoin, urlparse

class SiemensPLCDataScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_data = []
        
    def scrape_siemens_forums(self) -> List[Dict[str, Any]]:
        """Scrape Siemens forum discussions for PLC topics"""
        
        forum_urls = [
            "https://support.industry.siemens.com/tf/ww/en/threads/",
            "https://support.industry.siemens.com/tf/ww/en/posts/"
        ]
        
        scraped_discussions = []
        
        for base_url in forum_urls:
            try:
                # Search for PLC-related discussions
                search_terms = ["s7-1500", "s7-1200", "tia-portal", "profinet", "plc-programming"]
                
                for term in search_terms:
                    search_url = f"{base_url}?search={term}"
                    response = self.session.get(search_url, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Extract discussion threads
                        threads = soup.find_all('div', class_='thread-item')
                        
                        for thread in threads[:5]:  # Limit to 5 threads per search term
                            title_elem = thread.find('h3') or thread.find('h2')
                            content_elem = thread.find('p') or thread.find('div', class_='content')
                            
                            if title_elem and content_elem:
                                discussion = {
                                    'title': title_elem.get_text(strip=True),
                                    'content': content_elem.get_text(strip=True),
                                    'source': 'siemens_forum',
                                    'search_term': term,
                                    'url': search_url
                                }
                                scraped_discussions.append(discussion)
                    
                    time.sleep(1)  # Be respectful to the server
                    
            except Exception as e:
                print(f"Error scraping forum {base_url}: {e}")
        
        return scraped_discussions
    
    def scrape_automation_blogs(self) -> List[Dict[str, Any]]:
        """Scrape automation blogs for PLC content"""
        
        blog_urls = [
            "https://www.automation.com/en-us/articles",
            "https://www.controleng.com/articles",
            "https://www.automationworld.com/factory/article"
        ]
        
        scraped_articles = []
        
        for base_url in blog_urls:
            try:
                response = self.session.get(base_url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find article links
                    article_links = soup.find_all('a', href=True)
                    
                    for link in article_links[:10]:  # Limit to 10 articles per blog
                        href = link.get('href')
                        if href and ('plc' in href.lower() or 'siemens' in href.lower()):
                            full_url = urljoin(base_url, href)
                            
                            # Get article content
                            article_data = self.scrape_article_content(full_url)
                            if article_data:
                                scraped_articles.append(article_data)
                    
                    time.sleep(2)  # Be respectful to the server
                    
            except Exception as e:
                print(f"Error scraping blog {base_url}: {e}")
        
        return scraped_articles
    
    def scrape_article_content(self, url: str) -> Dict[str, Any]:
        """Scrape content from a specific article URL"""
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract title
                title_elem = soup.find('h1') or soup.find('title')
                title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
                
                # Extract main content
                content_selectors = [
                    'article', 'main', '.content', '.post-content', 
                    '.article-content', '.entry-content', 'section'
                ]
                
                content = ""
                for selector in content_selectors:
                    content_elem = soup.select_one(selector)
                    if content_elem:
                        # Remove script and style elements
                        for script in content_elem(["script", "style"]):
                            script.decompose()
                        content = content_elem.get_text(strip=True)
                        break
                
                # Filter for PLC-related content
                plc_keywords = ['plc', 'siemens', 's7-1500', 's7-1200', 'tia portal', 'profinet', 'automation']
                content_lower = content.lower()
                
                if any(keyword in content_lower for keyword in plc_keywords) and len(content) > 100:
                    return {
                        'title': title,
                        'content': content[:2000],  # Limit content length
                        'source': 'automation_blog',
                        'url': url
                    }
            
        except Exception as e:
            print(f"Error scraping article {url}: {e}")
        
        return None
    
    def scrape_github_repositories(self) -> List[Dict[str, Any]]:
        """Scrape GitHub repositories for PLC-related code and documentation"""
        
        github_searches = [
            "siemens+plc",
            "tia+portal",
            "s7-1500",
            "profinet+automation"
        ]
        
        scraped_repos = []
        
        for search_term in github_searches:
            try:
                # GitHub search API
                api_url = f"https://api.github.com/search/repositories?q={search_term}&sort=stars&order=desc"
                response = self.session.get(api_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for repo in data.get('items', [])[:5]:  # Limit to 5 repos per search
                        repo_data = {
                            'title': repo.get('name', 'Unknown'),
                            'content': f"Description: {repo.get('description', 'No description')}\n"
                                     f"Language: {repo.get('language', 'Unknown')}\n"
                                     f"Stars: {repo.get('stargazers_count', 0)}\n"
                                     f"Topics: {', '.join(repo.get('topics', []))}\n",
                            'source': 'github',
                            'url': repo.get('html_url', ''),
                            'stars': repo.get('stargazers_count', 0)
                        }
                        scraped_repos.append(repo_data)
                
                time.sleep(1)  # Respect GitHub API rate limits
                
            except Exception as e:
                print(f"Error scraping GitHub for {search_term}: {e}")
        
        return scraped_repos
    
    def scrape_youtube_transcripts(self) -> List[Dict[str, Any]]:
        """Scrape YouTube video information for PLC tutorials"""
        
        # Note: This is a simplified version. For actual transcript scraping,
        # you would need additional libraries like youtube-transcript-api
        
        youtube_searches = [
            "siemens plc programming tutorial",
            "tia portal tutorial",
            "s7-1500 programming",
            "profinet configuration tutorial"
        ]
        
        scraped_videos = []
        
        for search_term in youtube_searches:
            try:
                # YouTube search (simplified - normally would use YouTube API)
                search_url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
                response = self.session.get(search_url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract video titles and descriptions (simplified)
                    video_scripts = soup.find_all('script', type='application/ld+json')
                    
                    for script in video_scripts[:3]:  # Limit to 3 videos per search
                        try:
                            data = json.loads(script.string)
                            if isinstance(data, list):
                                for item in data:
                                    if item.get('@type') == 'VideoObject':
                                        video_data = {
                                            'title': item.get('name', 'Unknown Video'),
                                            'content': f"Description: {item.get('description', 'No description')}\n"
                                                     f"Duration: {item.get('duration', 'Unknown')}\n",
                                            'source': 'youtube',
                                            'url': item.get('url', ''),
                                            'search_term': search_term
                                        }
                                        scraped_videos.append(video_data)
                        except json.JSONDecodeError:
                            continue
                
                time.sleep(2)  # Be respectful to YouTube
                
            except Exception as e:
                print(f"Error scraping YouTube for {search_term}: {e}")
        
        return scraped_videos
    
    def scrape_all_sources(self) -> List[Dict[str, Any]]:
        """Scrape all available sources"""
        
        print("🌐 Starting comprehensive data scraping...")
        
        all_data = []
        
        # Scrape different sources
        print("📋 Scraping Siemens forums...")
        forum_data = self.scrape_siemens_forums()
        all_data.extend(forum_data)
        print(f"   Found {len(forum_data)} forum discussions")
        
        print("📰 Scraping automation blogs...")
        blog_data = self.scrape_automation_blogs()
        all_data.extend(blog_data)
        print(f"   Found {len(blog_data)} blog articles")
        
        print("💻 Scraping GitHub repositories...")
        github_data = self.scrape_github_repositories()
        all_data.extend(github_data)
        print(f"   Found {len(github_data)} repositories")
        
        print("🎥 Scraping YouTube content...")
        youtube_data = self.scrape_youtube_transcripts()
        all_data.extend(youtube_data)
        print(f"   Found {len(youtube_data)} videos")
        
        self.scraped_data = all_data
        print(f"✅ Total scraped items: {len(all_data)}")
        
        return all_data
    
    def save_scraped_data(self, filepath: str = "scraped_plc_data.json"):
        """Save scraped data to JSON file"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Scraped data saved to {filepath}")
    
    def load_scraped_data(self, filepath: str = "scraped_plc_data.json") -> List[Dict[str, Any]]:
        """Load scraped data from JSON file"""
        
        if Path(filepath).exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                self.scraped_data = json.load(f)
            
            print(f"📂 Loaded {len(self.scraped_data)} items from {filepath}")
            return self.scraped_data
        else:
            print(f"⚠️  File {filepath} not found")
            return []

def main():
    """Main function to run the scraper"""
    
    scraper = SiemensPLCDataScraper()
    
    # Try to load existing data first
    existing_data = scraper.load_scraped_data()
    
    if not existing_data:
        print("🚀 No existing data found, starting fresh scraping...")
        scraped_data = scraper.scrape_all_sources()
        scraper.save_scraped_data()
    else:
        print("📚 Using existing scraped data")
        print(f"   Total items: {len(existing_data)}")
        
        # Option to refresh data
        refresh = input("Refresh data? (y/n): ").lower().startswith('y')
        if refresh:
            scraped_data = scraper.scrape_all_sources()
            scraper.save_scraped_data()
    
    # Display summary
    if scraper.scraped_data:
        sources = {}
        for item in scraper.scraped_data:
            source = item.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print("\n📊 Data Summary:")
        for source, count in sources.items():
            print(f"   {source}: {count} items")

if __name__ == "__main__":
    main()
