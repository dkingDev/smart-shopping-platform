#!/usr/bin/env python3
"""
Smart Shopping Platform - Project Cleanup & Security Checker
Ensures the project remains clean and secure by checking for:
- Sensitive files that shouldn't be committed
- Proper .gitignore coverage
- Project structure compliance
"""

import os
import glob
import re
from pathlib import Path

class ProjectCleaner:
    def __init__(self, project_root="."):
        self.project_root = Path(project_root).resolve()
        
        # Sensitive file patterns that should NEVER be committed
        self.sensitive_patterns = [
            "*.env*", "!.env.example", "!.env.template",
            "*.pem", "*.key", "*.ppk", "*.crt",
            "*password*", "*secret*", "*token*",
            "config.ini", "config.json",
            "aws-credentials*", "cloudflare-secrets*",
            ".aws/", "*.tfvars"
        ]
        
        # Files that should be cleaned up
        self.cleanup_patterns = [
            "*.log", "*.tmp", "*.temp", "*.backup", "*.bak",
            "__pycache__/", "*.pyc", ".pytest_cache/",
            ".DS_Store", "Thumbs.db", "desktop.ini",
            "node_modules/", "dist/", "build/"
        ]
    
    def scan_sensitive_files(self):
        """Scan for files that contain sensitive information"""
        print("🔍 Scanning for sensitive files...")
        sensitive_files = []
        
        for pattern in self.sensitive_patterns:
            if pattern.startswith("!"):  # Skip exclusions
                continue
                
            matches = list(self.project_root.glob(f"**/{pattern}"))
            for match in matches:
                if match.is_file():
                    relative_path = match.relative_to(self.project_root)
                    sensitive_files.append(str(relative_path))
        
        return sensitive_files
    
    def check_gitignore_coverage(self):
        """Check if .gitignore properly covers sensitive files"""
        gitignore_path = self.project_root / ".gitignore"
        
        if not gitignore_path.exists():
            return False, "No .gitignore file found!"
        
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        missing_patterns = []
        for pattern in self.sensitive_patterns:
            if pattern.startswith("!"):  # Skip exclusions
                continue
            base_pattern = pattern.replace("**/", "").replace("**", "")
            if base_pattern not in gitignore_content:
                missing_patterns.append(pattern)
        
        return len(missing_patterns) == 0, missing_patterns
    
    def scan_for_hardcoded_secrets(self):
        """Scan code files for hardcoded secrets"""
        print("🔍 Scanning for hardcoded secrets...")
        
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'key\s*=\s*["\'][^"\']+["\']',
            r'aws_access_key_id\s*=\s*["\'][^"\']+["\']',
            r'aws_secret_access_key\s*=\s*["\'][^"\']+["\']'
        ]
        
        issues = []
        code_files = list(self.project_root.glob("**/*.py")) + \
                    list(self.project_root.glob("**/*.js")) + \
                    list(self.project_root.glob("**/*.sh"))
        
        for file_path in code_files:
            if ".git" in str(file_path) or "node_modules" in str(file_path):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for pattern in secret_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if "os.getenv" not in match.group() and "environment" not in match.group().lower():
                            relative_path = file_path.relative_to(self.project_root)
                            issues.append(f"{relative_path}: {match.group()}")
            except:
                continue
        
        return issues
    
    def cleanup_temporary_files(self):
        """Remove temporary and build files"""
        print("🧹 Cleaning up temporary files...")
        cleaned = []
        
        for pattern in self.cleanup_patterns:
            matches = list(self.project_root.glob(f"**/{pattern}"))
            for match in matches:
                try:
                    if match.is_file():
                        match.unlink()
                        cleaned.append(str(match.relative_to(self.project_root)))
                    elif match.is_dir():
                        import shutil
                        shutil.rmtree(match)
                        cleaned.append(str(match.relative_to(self.project_root)))
                except:
                    continue
        
        return cleaned
    
    def generate_security_report(self):
        """Generate a comprehensive security report"""
        print("📋 Generating security report...")
        
        report = []
        report.append("# 🔒 Smart Shopping Platform - Security Report")
        report.append(f"Generated: {os.environ.get('DATE', 'Unknown')}")
        report.append("")
        
        # Check sensitive files
        sensitive_files = self.scan_sensitive_files()
        if sensitive_files:
            report.append("## ⚠️ SENSITIVE FILES DETECTED")
            report.append("The following files contain sensitive information:")
            for file in sensitive_files:
                report.append(f"- `{file}`")
            report.append("")
            report.append("**ACTION REQUIRED**: Ensure these files are in .gitignore and not committed!")
            report.append("")
        else:
            report.append("## ✅ NO SENSITIVE FILES DETECTED")
            report.append("")
        
        # Check .gitignore coverage
        is_covered, missing = self.check_gitignore_coverage()
        if not is_covered:
            report.append("## ⚠️ GITIGNORE NEEDS UPDATE")
            if isinstance(missing, str):
                report.append(missing)
            else:
                report.append("Missing patterns:")
                for pattern in missing:
                    report.append(f"- `{pattern}`")
            report.append("")
        else:
            report.append("## ✅ GITIGNORE PROPERLY CONFIGURED")
            report.append("")
        
        # Check for hardcoded secrets
        secret_issues = self.scan_for_hardcoded_secrets()
        if secret_issues:
            report.append("## ⚠️ POTENTIAL HARDCODED SECRETS")
            for issue in secret_issues:
                report.append(f"- `{issue}`")
            report.append("")
        else:
            report.append("## ✅ NO HARDCODED SECRETS DETECTED")
            report.append("")
        
        return "\n".join(report)
    
    def run_full_cleanup(self):
        """Run complete project cleanup and security check"""
        print("🚀 Starting Smart Shopping Platform cleanup...")
        print("=" * 50)
        
        # Clean temporary files
        cleaned = self.cleanup_temporary_files()
        if cleaned:
            print(f"✅ Cleaned {len(cleaned)} temporary files")
        
        # Generate security report
        report = self.generate_security_report()
          # Save report
        report_path = self.project_root / "docs" / "SECURITY-REPORT.md"
        report_path.parent.mkdir(exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📋 Security report saved to: {report_path}")
        print("=" * 50)
        print("🎉 Project cleanup completed!")
        
        return report

if __name__ == "__main__":
    cleaner = ProjectCleaner()
    report = cleaner.run_full_cleanup()
    print("\n" + report)
