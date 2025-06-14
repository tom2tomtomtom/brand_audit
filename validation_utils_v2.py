#!/usr/bin/env python3
"""
Validation Utilities for Brand Audit V2
Ensures data quality and authenticity
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlparse
import json

class BrandDataValidator:
    """Validates extracted brand data to ensure quality and authenticity"""
    
    def __init__(self):
        # Placeholder patterns to detect and reject
        self.placeholder_patterns = [
            r'lorem\s+ipsum',
            r'your\s+(company|brand|business)',
            r'example\.com',
            r'coming\s+soon',
            r'under\s+construction',
            r'placeholder',
            r'sample\s+text',
            r'insert\s+(text|content)',
            r'default',
            r'\[.*\]',  # Brackets often indicate placeholders
            r'\{.*\}',  # Curly braces
            r'xxx+',
            r'tbd|TBD',
            r'n/a|N/A'
        ]
        
        # Quality thresholds
        self.min_text_length = {
            'company_name': 2,
            'positioning': 20,
            'value_proposition': 20,
            'messages': 10,
            'description': 30
        }
        
        self.max_text_length = {
            'company_name': 100,
            'positioning': 500,
            'value_proposition': 300,
            'messages': 300
        }
    
    def validate_extraction(self, data: Dict[str, Any], strict: bool = True) -> Tuple[bool, List[str]]:
        """
        Validate extracted data
        Returns: (is_valid, list_of_issues)
        """
        issues = []
        
        if not data:
            return False, ["No data provided"]
        
        # Check for minimum required fields
        if strict:
            required_fields = ['company_name', 'positioning']
            for field in required_fields:
                if field not in data or not data[field]:
                    issues.append(f"Missing required field: {field}")
        
        # Validate each field
        for field, value in data.items():
            field_issues = self._validate_field(field, value)
            issues.extend(field_issues)
        
        # Check overall data quality
        quality_score = self.calculate_quality_score(data)
        if quality_score < 0.3:
            issues.append(f"Overall quality score too low: {quality_score:.2f}")
        
        return len(issues) == 0, issues
    
    def _validate_field(self, field_name: str, value: Any) -> List[str]:
        """Validate individual field"""
        issues = []
        
        if value is None:
            return issues  # None is acceptable for optional fields
        
        # String fields
        if isinstance(value, str):
            # Check for empty or whitespace only
            if not value.strip():
                issues.append(f"{field_name}: Empty or whitespace only")
                return issues
            
            # Check for placeholders
            for pattern in self.placeholder_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    issues.append(f"{field_name}: Contains placeholder text (pattern: {pattern})")
            
            # Check length
            if field_name in self.min_text_length:
                if len(value) < self.min_text_length[field_name]:
                    issues.append(f"{field_name}: Too short ({len(value)} < {self.min_text_length[field_name]})")
            
            if field_name in self.max_text_length:
                if len(value) > self.max_text_length[field_name]:
                    issues.append(f"{field_name}: Too long ({len(value)} > {self.max_text_length[field_name]})")
            
            # Field-specific validation
            if field_name == 'company_name':
                issues.extend(self._validate_company_name(value))
            elif field_name == 'url' or field_name.endswith('_url'):
                issues.extend(self._validate_url(value))
            elif field_name == 'email':
                issues.extend(self._validate_email(value))
            elif field_name == 'phone':
                issues.extend(self._validate_phone(value))
        
        # List fields
        elif isinstance(value, list):
            if not value:
                issues.append(f"{field_name}: Empty list")
            else:
                # Validate each item
                for i, item in enumerate(value):
                    if isinstance(item, str):
                        item_issues = self._validate_field(f"{field_name}[{i}]", item)
                        issues.extend(item_issues)
                
                # Check for duplicate items
                if len(value) != len(set(str(v) for v in value)):
                    issues.append(f"{field_name}: Contains duplicate values")
        
        # Color validation
        if field_name == 'colors' and isinstance(value, list):
            issues.extend(self._validate_colors(value))
        
        return issues
    
    def _validate_company_name(self, name: str) -> List[str]:
        """Validate company name"""
        issues = []
        
        # Check for common invalid patterns
        invalid_patterns = [
            r'^\d+$',  # Only numbers
            r'^www\.',  # Starts with www.
            r'\.com$',  # Ends with .com
            r'^https?://',  # URL instead of name
            r'[<>"]',  # HTML tags or quotes
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, name, re.IGNORECASE):
                issues.append(f"Company name has invalid format: {pattern}")
        
        # Check for reasonable company name
        if len(name.split()) > 10:
            issues.append("Company name unreasonably long")
        
        return issues
    
    def _validate_url(self, url: str) -> List[str]:
        """Validate URL format"""
        issues = []
        
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                issues.append("Invalid URL format")
            elif result.scheme not in ['http', 'https']:
                issues.append("URL must use http or https")
        except:
            issues.append("Cannot parse URL")
        
        return issues
    
    def _validate_email(self, email: str) -> List[str]:
        """Validate email format"""
        issues = []
        
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            issues.append("Invalid email format")
        
        # Check for placeholder emails
        if any(domain in email.lower() for domain in ['example.com', 'test.com', 'localhost']):
            issues.append("Placeholder email domain")
        
        return issues
    
    def _validate_phone(self, phone: str) -> List[str]:
        """Validate phone number"""
        issues = []
        
        # Remove all non-digits
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) < 10:
            issues.append("Phone number too short")
        elif len(digits) > 15:
            issues.append("Phone number too long")
        
        # Check for placeholder patterns
        if re.search(r'(123456789|000000|111111|999999)', digits):
            issues.append("Placeholder phone number pattern")
        
        return issues
    
    def _validate_colors(self, colors: List[str]) -> List[str]:
        """Validate color values"""
        issues = []
        
        valid_colors = []
        for color in colors:
            if self._is_valid_color(color):
                valid_colors.append(color)
            else:
                issues.append(f"Invalid color format: {color}")
        
        # Check for reasonable color palette
        if len(valid_colors) > 10:
            issues.append("Too many colors (>10)")
        
        # Check for diversity (not all grays)
        if valid_colors:
            gray_count = sum(1 for c in valid_colors if self._is_grayscale(c))
            if gray_count == len(valid_colors):
                issues.append("Color palette contains only grayscale colors")
        
        return issues
    
    def _is_valid_color(self, color: str) -> bool:
        """Check if color format is valid"""
        # Hex color
        if re.match(r'^#[0-9A-Fa-f]{6}$', color):
            return True
        # RGB/RGBA
        if re.match(r'^rgba?\(\d+,\s*\d+,\s*\d+', color):
            return True
        return False
    
    def _is_grayscale(self, color: str) -> bool:
        """Check if color is grayscale"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            # Check if R, G, B are very close
            return max(abs(r-g), abs(g-b), abs(r-b)) < 10
        return False
    
    def calculate_quality_score(self, data: Dict[str, Any]) -> float:
        """Calculate overall quality score (0-1)"""
        scores = []
        
        # Check completeness
        expected_fields = [
            'company_name', 'positioning', 'value_proposition',
            'messages', 'colors', 'logo_url', 'target_audience'
        ]
        
        present_fields = sum(1 for field in expected_fields if data.get(field))
        completeness_score = present_fields / len(expected_fields)
        scores.append(completeness_score)
        
        # Check field quality
        field_scores = []
        for field, value in data.items():
            if value:
                field_score = self._calculate_field_quality(field, value)
                field_scores.append(field_score)
        
        if field_scores:
            scores.append(sum(field_scores) / len(field_scores))
        
        # Check for rich content
        rich_content_score = 0
        if data.get('messages') and len(data['messages']) >= 3:
            rich_content_score += 0.3
        if data.get('colors') and len(data['colors']) >= 3:
            rich_content_score += 0.3
        if data.get('target_audience') and len(data['target_audience']) >= 2:
            rich_content_score += 0.2
        if data.get('personality_traits'):
            rich_content_score += 0.2
        scores.append(rich_content_score)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _calculate_field_quality(self, field: str, value: Any) -> float:
        """Calculate quality score for individual field"""
        if isinstance(value, str):
            # Check length relative to expected
            if field in self.min_text_length and field in self.max_text_length:
                min_len = self.min_text_length[field]
                max_len = self.max_text_length[field]
                optimal_len = (min_len + max_len) / 2
                
                if len(value) < min_len:
                    return 0.0
                elif len(value) > max_len:
                    return 0.5
                else:
                    # Score based on how close to optimal length
                    distance_from_optimal = abs(len(value) - optimal_len)
                    max_distance = optimal_len - min_len
                    return 1.0 - (distance_from_optimal / max_distance) * 0.5
            else:
                # Default scoring for other string fields
                if len(value) < 5:
                    return 0.3
                elif len(value) < 20:
                    return 0.6
                else:
                    return 1.0
        
        elif isinstance(value, list):
            if not value:
                return 0.0
            # Score based on number of items and their quality
            item_scores = []
            for item in value[:10]:  # Check up to 10 items
                if isinstance(item, str) and len(item) > 5:
                    item_scores.append(1.0)
                else:
                    item_scores.append(0.3)
            
            return sum(item_scores) / len(item_scores) if item_scores else 0.0
        
        else:
            # Default score for other types
            return 0.5 if value else 0.0
    
    def validate_against_source(self, extracted_data: Dict[str, Any], 
                               source_content: str) -> Tuple[bool, List[str]]:
        """Validate extracted data against source content"""
        issues = []
        
        if not source_content:
            return True, []  # Can't validate without source
        
        source_lower = source_content.lower()
        
        # Validate company name appears in source
        if extracted_data.get('company_name'):
            name = extracted_data['company_name']
            if name.lower() not in source_lower:
                # Try variations
                name_parts = name.split()
                if not any(part.lower() in source_lower for part in name_parts if len(part) > 3):
                    issues.append("Company name not found in source content")
        
        # Validate messages are from source
        if extracted_data.get('messages'):
            for i, message in enumerate(extracted_data['messages']):
                # Allow some flexibility for AI paraphrasing
                message_words = [w for w in message.lower().split() if len(w) > 4]
                if message_words:
                    found_words = sum(1 for word in message_words if word in source_lower)
                    if found_words / len(message_words) < 0.5:
                        issues.append(f"Message {i+1} doesn't match source content")
        
        return len(issues) == 0, issues
    
    def clean_extracted_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and normalize extracted data"""
        cleaned = {}
        
        for key, value in data.items():
            if value is None or value == "" or value == []:
                continue
            
            if isinstance(value, str):
                # Clean whitespace
                cleaned_value = ' '.join(value.split())
                
                # Remove HTML entities
                cleaned_value = re.sub(r'&[a-zA-Z]+;', '', cleaned_value)
                
                # Remove excess punctuation
                cleaned_value = re.sub(r'[.!?]{2,}', '.', cleaned_value)
                
                if cleaned_value:
                    cleaned[key] = cleaned_value
            
            elif isinstance(value, list):
                cleaned_list = []
                for item in value:
                    if isinstance(item, str):
                        cleaned_item = ' '.join(item.split())
                        if cleaned_item and cleaned_item not in cleaned_list:
                            cleaned_list.append(cleaned_item)
                    elif item is not None:
                        if item not in cleaned_list:
                            cleaned_list.append(item)
                
                if cleaned_list:
                    cleaned[key] = cleaned_list
            
            else:
                cleaned[key] = value
        
        return cleaned
    
    def merge_extraction_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple extraction results intelligently"""
        if not results:
            return {}
        
        if len(results) == 1:
            return results[0]
        
        merged = {}
        
        # Define merge strategies for different fields
        merge_strategies = {
            'company_name': self._merge_by_consensus,
            'positioning': self._merge_longest,
            'value_proposition': self._merge_longest,
            'messages': self._merge_lists,
            'colors': self._merge_lists,
            'target_audience': self._merge_lists,
            'personality_traits': self._merge_lists,
            'logo_url': self._merge_first_valid,
            'email': self._merge_first_valid,
            'phone': self._merge_first_valid
        }
        
        # Collect all fields
        all_fields = set()
        for result in results:
            all_fields.update(result.keys())
        
        # Merge each field
        for field in all_fields:
            values = [r.get(field) for r in results if r.get(field)]
            
            if not values:
                continue
            
            if field in merge_strategies:
                merged_value = merge_strategies[field](values)
            else:
                # Default: take first non-null value
                merged_value = values[0]
            
            if merged_value:
                merged[field] = merged_value
        
        return merged
    
    def _merge_by_consensus(self, values: List[Any]) -> Any:
        """Merge by finding most common value"""
        if not values:
            return None
        
        # Count occurrences
        from collections import Counter
        counts = Counter(values)
        
        # Return most common
        return counts.most_common(1)[0][0]
    
    def _merge_longest(self, values: List[str]) -> str:
        """Merge by taking longest value"""
        if not values:
            return ""
        
        return max(values, key=len)
    
    def _merge_lists(self, values: List[List[Any]]) -> List[Any]:
        """Merge lists by combining unique values"""
        merged = []
        seen = set()
        
        for value_list in values:
            if isinstance(value_list, list):
                for item in value_list:
                    item_str = str(item)
                    if item_str not in seen:
                        seen.add(item_str)
                        merged.append(item)
        
        return merged
    
    def _merge_first_valid(self, values: List[Any]) -> Any:
        """Take first valid (non-empty) value"""
        for value in values:
            if value:
                return value
        return None
    
    def generate_validation_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed validation report"""
        is_valid, issues = self.validate_extraction(data)
        quality_score = self.calculate_quality_score(data)
        
        report = {
            'is_valid': is_valid,
            'quality_score': quality_score,
            'quality_grade': self._score_to_grade(quality_score),
            'total_issues': len(issues),
            'issues': issues,
            'field_analysis': self._analyze_fields(data),
            'recommendations': self._generate_recommendations(data, issues, quality_score)
        }
        
        return report
    
    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 0.9:
            return 'A'
        elif score >= 0.8:
            return 'B'
        elif score >= 0.7:
            return 'C'
        elif score >= 0.6:
            return 'D'
        else:
            return 'F'
    
    def _analyze_fields(self, data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Analyze each field in detail"""
        analysis = {}
        
        for field, value in data.items():
            field_analysis = {
                'present': True,
                'type': type(value).__name__,
                'quality_score': self._calculate_field_quality(field, value)
            }
            
            if isinstance(value, str):
                field_analysis['length'] = len(value)
                field_analysis['word_count'] = len(value.split())
            elif isinstance(value, list):
                field_analysis['item_count'] = len(value)
                if value and isinstance(value[0], str):
                    field_analysis['avg_item_length'] = sum(len(v) for v in value) / len(value)
            
            analysis[field] = field_analysis
        
        return analysis
    
    def _generate_recommendations(self, data: Dict[str, Any], 
                                 issues: List[str], 
                                 quality_score: float) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []
        
        if quality_score < 0.5:
            recommendations.append("Consider re-extracting with different strategies")
        
        # Field-specific recommendations
        if not data.get('company_name'):
            recommendations.append("Company name is critical - verify extraction methods")
        
        if not data.get('positioning') or len(data.get('positioning', '')) < 50:
            recommendations.append("Positioning statement is too brief - look for hero content")
        
        if not data.get('messages') or len(data.get('messages', [])) < 3:
            recommendations.append("Extract more key messages from headings and feature sections")
        
        if not data.get('colors'):
            recommendations.append("Consider visual extraction methods for brand colors")
        
        if not data.get('target_audience'):
            recommendations.append("Look for audience indicators in about/features sections")
        
        # Issue-based recommendations
        if any('placeholder' in issue.lower() for issue in issues):
            recommendations.append("Source may contain placeholder content - verify site is live")
        
        if any('too short' in issue.lower() for issue in issues):
            recommendations.append("Content may be minimal - try extracting from multiple pages")
        
        return recommendations


class ExtractionValidator:
    """Validates extraction process and results"""
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, Optional[str]]:
        """Validate URL before extraction"""
        try:
            result = urlparse(url)
            
            if not all([result.scheme, result.netloc]):
                return False, "Invalid URL format"
            
            if result.scheme not in ['http', 'https']:
                return False, "URL must use http or https"
            
            # Check for localhost/private IPs
            if any(private in result.netloc for private in ['localhost', '127.0.0.1', '192.168.', '10.', '172.']):
                return False, "Cannot extract from localhost or private IPs"
            
            return True, None
            
        except Exception as e:
            return False, f"URL parsing error: {str(e)}"
    
    @staticmethod
    def validate_extraction_result(result: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate extraction result structure"""
        issues = []
        
        # Check required fields
        required_fields = ['status', 'url', 'timestamp']
        for field in required_fields:
            if field not in result:
                issues.append(f"Missing required field: {field}")
        
        # Check status
        if result.get('status') not in ['success', 'partial_success', 'failed']:
            issues.append("Invalid status value")
        
        # For successful extractions, check data
        if result.get('status') in ['success', 'partial_success']:
            if 'data' not in result:
                issues.append("Success status but no data field")
            elif not isinstance(result['data'], dict):
                issues.append("Data field must be a dictionary")
        
        return len(issues) == 0, issues
    
    @staticmethod
    def calculate_extraction_confidence(result: Dict[str, Any]) -> float:
        """Calculate confidence in extraction result"""
        if result.get('status') == 'failed':
            return 0.0
        
        confidence = 0.0
        
        # Base confidence from status
        if result.get('status') == 'success':
            confidence = 0.7
        elif result.get('status') == 'partial_success':
            confidence = 0.4
        
        # Adjust based on extraction methods
        methods = result.get('extraction_methods_attempted', [])
        if 'selenium_extraction' in methods:
            confidence += 0.1
        if 'visual_analysis' in methods:
            confidence += 0.1
        if 'structured_data' in methods:
            confidence += 0.1
        
        # Adjust based on data completeness
        if result.get('data'):
            data = result['data']
            if data.get('company_name'):
                confidence += 0.05
            if data.get('positioning'):
                confidence += 0.05
            if data.get('messages'):
                confidence += 0.05
        
        # Cap at 1.0
        return min(confidence, 1.0)
