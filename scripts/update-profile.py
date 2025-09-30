#!/usr/bin/env python3
"""
GitHub Profile README Update Script
Automatically updates GitHub profile README with dynamic content
"""

import os
import sys
import yaml
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

class GitHubProfileUpdater:
    def __init__(self, config_path: str):
        """Initialize the profile updater with configuration."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.username = self.config['profile']['username']
        self.github_token = os.getenv('GITHUB_TOKEN')

        if not self.github_token:
            print("Warning: GITHUB_TOKEN not found. Some features may be limited.")

    def get_github_stats(self) -> Dict:
        """Fetch GitHub statistics for the user."""
        if not self.github_token:
            return {}

        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        try:
            # Get user info
            user_response = requests.get(
                f'https://api.github.com/users/{self.username}',
                headers=headers
            )
            user_data = user_response.json()

            # Get repositories
            repos_response = requests.get(
                f'https://api.github.com/users/{self.username}/repos?per_page=100',
                headers=headers
            )
            repos_data = repos_response.json()

            # Calculate stats
            total_stars = sum(repo['stargazers_count'] for repo in repos_data)
            total_forks = sum(repo['forks_count'] for repo in repos_data)

            return {
                'public_repos': user_data.get('public_repos', 0),
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'total_stars': total_stars,
                'total_forks': total_forks
            }
        except Exception as e:
            print(f"Error fetching GitHub stats: {e}")
            return {}

    def get_latest_blog_posts(self, feed_url: str, count: int = 5) -> List[Dict]:
        """Fetch latest blog posts from RSS/Atom feed."""
        try:
            import feedparser
            feed = feedparser.parse(feed_url)

            posts = []
            for entry in feed.entries[:count]:
                posts.append({
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published if hasattr(entry, 'published') else ''
                })
            return posts
        except ImportError:
            print("feedparser not installed. Skipping blog posts.")
            return []
        except Exception as e:
            print(f"Error fetching blog posts: {e}")
            return []

    def generate_skills_section(self) -> str:
        """Generate the skills section with badges."""
        skills_html = ""

        for category, skills in self.config['skills'].items():
            if category == 'primary':
                skills_html += "### Core Languages & Frameworks\n"
            elif category == 'frameworks':
                skills_html += "\n### Backend & Frontend\n"
            elif category == 'cloud_devops':
                skills_html += "\n### Cloud & DevOps\n"
            elif category == 'ai_ml':
                skills_html += "\n### AI & Machine Learning\n"

            for skill in skills:
                badge_name = skill.replace(' ', '_').replace('.', '')
                skills_html += f"![{skill}](https://img.shields.io/badge/{skill}-{self.config['theme']['primary_color'].replace('#', '')}?style=for-the-badge&logo={skill.lower()}&logoColor=white)\n"

        return skills_html

    def generate_projects_section(self) -> str:
        """Generate the featured projects section."""
        projects_html = "<table>\n<tr>\n"

        for i, project in enumerate(self.config['featured_projects']):
            if i % 2 == 0 and i > 0:
                projects_html += "</tr>\n<tr>\n"

            projects_html += "<td width=\"50%\">\n\n"
            projects_html += f"### {project['name']}\n"
            projects_html += f"**{project['description']}**\n"
            projects_html += f"- **Tech:** {', '.join(project['tech_stack'])}\n"
            projects_html += f"- **Status:** {project['status']}\n\n"
            projects_html += "</td>\n"

        projects_html += "</tr>\n</table>\n"
        return projects_html

    def update_readme(self, template_path: str, output_path: str):
        """Update the README file with current data."""
        try:
            # Read template
            with open(template_path, 'r') as f:
                template = f.read()

            # Get dynamic data
            stats = self.get_github_stats()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

            # Replace placeholders
            updated_content = template.replace(
                "{{LAST_UPDATED}}", f"Last updated: {current_time}"
            )

            # Add stats if available
            if stats:
                stats_section = f"""
### 📊 Quick Stats
- 🚀 **{stats['public_repos']}** Public Repositories
- ⭐ **{stats['total_stars']}** Total Stars Earned
- 👥 **{stats['followers']}** Followers
- 🔀 **{stats['total_forks']}** Total Forks
"""
                updated_content = updated_content.replace(
                    "{{STATS_SECTION}}", stats_section
                )

            # Write updated README
            with open(output_path, 'w') as f:
                f.write(updated_content)

            print(f"✅ README updated successfully at {output_path}")

        except Exception as e:
            print(f"❌ Error updating README: {e}")

    def validate_links(self) -> Dict[str, bool]:
        """Validate all external links in the profile."""
        links_to_check = []

        # Add social links
        for platform, url in self.config['social_links'].items():
            if url and url.startswith('http'):
                links_to_check.append((platform, url))

        # Add organization links
        for org in self.config['organizations']:
            links_to_check.append((org['name'], org['url']))

        results = {}
        for name, url in links_to_check:
            try:
                response = requests.head(url, timeout=10)
                results[name] = response.status_code < 400
            except:
                results[name] = False

        return results

    def generate_report(self) -> str:
        """Generate a profile health report."""
        stats = self.get_github_stats()
        link_status = self.validate_links()

        report = f"""
# GitHub Profile Health Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Profile Statistics
- Public Repositories: {stats.get('public_repos', 'N/A')}
- Total Stars: {stats.get('total_stars', 'N/A')}
- Followers: {stats.get('followers', 'N/A')}

## Link Validation
"""

        for name, status in link_status.items():
            status_emoji = "✅" if status else "❌"
            report += f"- {status_emoji} {name}\n"

        return report

def main():
    """Main function to run the profile updater."""
    if len(sys.argv) < 2:
        print("Usage: python update-profile.py <config-file> [command]")
        print("Commands: update, validate, report")
        sys.exit(1)

    config_file = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else 'update'

    updater = GitHubProfileUpdater(config_file)

    if command == 'update':
        template_path = os.path.join(os.path.dirname(config_file), 'README.md')
        output_path = os.path.join(os.path.dirname(config_file), 'README_updated.md')
        updater.update_readme(template_path, output_path)

    elif command == 'validate':
        results = updater.validate_links()
        print("\n🔍 Link Validation Results:")
        for name, status in results.items():
            status_emoji = "✅" if status else "❌"
            print(f"{status_emoji} {name}")

    elif command == 'report':
        report = updater.generate_report()
        print(report)

        # Save report to file
        report_path = os.path.join(os.path.dirname(config_file), 'profile_report.md')
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\n📊 Report saved to: {report_path}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()