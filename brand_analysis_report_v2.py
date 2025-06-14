#!/usr/bin/env python3
"""
Brand Analysis Report Generator V2 - Real Data Only
No placeholders, no defaults - only extracted data
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import statistics

class BrandAnalysisReportV2:
    def __init__(self):
        self.report_timestamp = datetime.now().isoformat()
        
    def generate_report(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive report from analysis results"""
        
        # Separate successful and failed analyses
        successful = [r for r in analysis_results if r.get('status') == 'success']
        failed = [r for r in analysis_results if r.get('status') != 'success']
        
        if not successful:
            return {
                'status': 'no_data',
                'message': 'No brands could be successfully analyzed',
                'timestamp': self.report_timestamp,
                'attempted_count': len(analysis_results),
                'failures': self._summarize_failures(failed)
            }
        
        return {
            'status': 'success',
            'timestamp': self.report_timestamp,
            'summary': self._generate_summary(successful, failed),
            'brand_profiles': self._enhance_profiles(successful),
            'competitive_landscape': self._analyze_landscape(successful),
            'market_insights': self._extract_market_insights(successful),
            'quality_metrics': self._calculate_quality_metrics(successful),
            'extraction_details': self._get_extraction_details(analysis_results)
        }
    
    def _generate_summary(self, successful: List[Dict], failed: List[Dict]) -> Dict[str, Any]:
        """Generate executive summary"""
        return {
            'total_brands_analyzed': len(successful) + len(failed),
            'successful_extractions': len(successful),
            'failed_extractions': len(failed),
            'extraction_rate': len(successful) / (len(successful) + len(failed)) if successful or failed else 0,
            'data_completeness': self._calculate_completeness(successful),
            'industries_detected': self._get_unique_industries(successful),
            'analysis_depth': self._assess_analysis_depth(successful)
        }
    
    def _enhance_profiles(self, profiles: List[Dict]) -> List[Dict]:
        """Enhance brand profiles with comparative metrics"""
        enhanced = []
        
        for profile in profiles:
            enhanced_profile = profile.copy()
            
            # Add comparative metrics
            enhanced_profile['comparative_metrics'] = {
                'positioning_clarity': self._assess_positioning_clarity(profile),
                'message_consistency': self._assess_message_consistency(profile),
                'value_prop_strength': self._assess_value_prop_strength(profile),
                'brand_differentiation': self._assess_differentiation(profile, profiles)
            }
            
            # Add extraction quality indicators
            enhanced_profile['data_quality'] = {
                'completeness_score': self._calculate_profile_completeness(profile),
                'confidence_level': profile.get('extraction_confidence', 0),
                'data_sources': self._list_data_sources(profile)
            }
            
            enhanced.append(enhanced_profile)
        
        return enhanced
    
    def _analyze_landscape(self, profiles: List[Dict]) -> Dict[str, Any]:
        """Analyze competitive landscape from extracted data"""
        if len(profiles) < 2:
            return {'status': 'insufficient_data', 'message': 'Need at least 2 brands for landscape analysis'}
        
        landscape = {
            'positioning_map': self._create_positioning_map(profiles),
            'common_themes': self._identify_common_themes(profiles),
            'differentiation_factors': self._identify_differentiation_factors(profiles),
            'market_maturity_indicators': self._assess_market_maturity(profiles),
            'competitive_gaps': self._identify_gaps(profiles)
        }
        
        return landscape
    
    def _extract_market_insights(self, profiles: List[Dict]) -> Dict[str, Any]:
        """Extract market-level insights from brand data"""
        insights = {
            'dominant_value_propositions': self._analyze_value_props(profiles),
            'messaging_patterns': self._analyze_messaging_patterns(profiles),
            'target_audience_overlaps': self._analyze_audience_overlaps(profiles),
            'technology_adoption': self._analyze_tech_mentions(profiles),
            'market_positioning_clusters': self._identify_positioning_clusters(profiles)
        }
        
        return insights
    
    def _calculate_quality_metrics(self, profiles: List[Dict]) -> Dict[str, Any]:
        """Calculate overall data quality metrics"""
        completeness_scores = [self._calculate_profile_completeness(p) for p in profiles]
        confidence_scores = [p.get('extraction_confidence', 0) for p in profiles]
        
        return {
            'average_completeness': statistics.mean(completeness_scores) if completeness_scores else 0,
            'completeness_std_dev': statistics.stdev(completeness_scores) if len(completeness_scores) > 1 else 0,
            'average_confidence': statistics.mean(confidence_scores) if confidence_scores else 0,
            'high_quality_profiles': len([s for s in completeness_scores if s > 0.8]),
            'low_quality_profiles': len([s for s in completeness_scores if s < 0.5]),
            'data_coverage': self._assess_data_coverage(profiles)
        }
    
    def _get_extraction_details(self, all_results: List[Dict]) -> Dict[str, Any]:
        """Provide detailed extraction information"""
        return {
            'extraction_methods_used': self._summarize_methods(all_results),
            'failure_analysis': self._analyze_failures(all_results),
            'extraction_duration': self._calculate_duration(all_results),
            'retry_attempts': self._count_retries(all_results)
        }
    
    # Helper methods for detailed analysis
    
    def _calculate_completeness(self, profiles: List[Dict]) -> float:
        """Calculate overall data completeness"""
        if not profiles:
            return 0.0
            
        required_fields = ['company_name', 'positioning', 'value_proposition', 'messages', 'colors']
        total_fields = len(required_fields) * len(profiles)
        filled_fields = 0
        
        for profile in profiles:
            for field in required_fields:
                if profile.get(field) and profile[field] not in [None, '', [], {}]:
                    filled_fields += 1
        
        return filled_fields / total_fields if total_fields > 0 else 0.0
    
    def _get_unique_industries(self, profiles: List[Dict]) -> List[str]:
        """Extract unique industries detected"""
        industries = set()
        for profile in profiles:
            if profile.get('industry_detected'):
                industries.add(profile['industry_detected'])
        return list(industries)
    
    def _assess_analysis_depth(self, profiles: List[Dict]) -> str:
        """Assess the depth of analysis achieved"""
        if not profiles:
            return "none"
            
        depth_scores = []
        for profile in profiles:
            score = 0
            if profile.get('positioning'): score += 1
            if profile.get('personality_traits'): score += 1
            if profile.get('value_proposition'): score += 1
            if profile.get('target_audience'): score += 1
            if profile.get('competitive_analysis'): score += 1
            depth_scores.append(score)
        
        avg_score = statistics.mean(depth_scores)
        if avg_score >= 4: return "comprehensive"
        elif avg_score >= 3: return "detailed"
        elif avg_score >= 2: return "moderate"
        elif avg_score >= 1: return "basic"
        else: return "minimal"
    
    def _assess_positioning_clarity(self, profile: Dict) -> float:
        """Assess clarity of brand positioning"""
        score = 0.0
        
        if profile.get('positioning'):
            positioning = profile['positioning']
            # Check for specific, actionable positioning
            if len(positioning) > 50: score += 0.3
            if any(word in positioning.lower() for word in ['unique', 'only', 'first', 'best']): 
                score += 0.2
            if profile.get('value_proposition'): score += 0.3
            if profile.get('differentiation_factors'): score += 0.2
        
        return min(score, 1.0)
    
    def _assess_message_consistency(self, profile: Dict) -> float:
        """Assess consistency across brand messages"""
        messages = profile.get('messages', [])
        if not messages:
            return 0.0
        
        # Extract key terms from positioning
        positioning = profile.get('positioning', '')
        key_terms = set(word.lower() for word in positioning.split() if len(word) > 4)
        
        # Check how many messages align with positioning
        aligned_messages = 0
        for message in messages:
            message_terms = set(word.lower() for word in message.split() if len(word) > 4)
            if key_terms & message_terms:  # Intersection
                aligned_messages += 1
        
        return aligned_messages / len(messages) if messages else 0.0
    
    def _assess_value_prop_strength(self, profile: Dict) -> float:
        """Assess strength of value proposition"""
        value_prop = profile.get('value_proposition', '')
        if not value_prop:
            return 0.0
        
        score = 0.0
        
        # Check for specificity
        if len(value_prop) > 30: score += 0.2
        
        # Check for benefit-oriented language
        benefit_words = ['increase', 'reduce', 'improve', 'enhance', 'save', 'gain', 'achieve']
        if any(word in value_prop.lower() for word in benefit_words):
            score += 0.3
        
        # Check for quantification
        import re
        if re.search(r'\d+', value_prop):  # Contains numbers
            score += 0.2
        
        # Check for target audience mention
        audience_indicators = ['for', 'helps', 'enables']
        if any(word in value_prop.lower() for word in audience_indicators):
            score += 0.3
        
        return min(score, 1.0)
    
    def _assess_differentiation(self, profile: Dict, all_profiles: List[Dict]) -> float:
        """Assess how differentiated this brand is from others"""
        if len(all_profiles) < 2:
            return 0.5  # Neutral score if no comparison possible
        
        # Get this brand's key terms
        positioning = profile.get('positioning', '') + ' ' + profile.get('value_proposition', '')
        brand_terms = set(word.lower() for word in positioning.split() if len(word) > 5)
        
        if not brand_terms:
            return 0.0
        
        # Compare with other brands
        overlap_scores = []
        for other in all_profiles:
            if other.get('company_name') != profile.get('company_name'):
                other_positioning = other.get('positioning', '') + ' ' + other.get('value_proposition', '')
                other_terms = set(word.lower() for word in other_positioning.split() if len(word) > 5)
                
                if other_terms:
                    overlap = len(brand_terms & other_terms) / len(brand_terms)
                    overlap_scores.append(overlap)
        
        # Lower overlap = higher differentiation
        avg_overlap = statistics.mean(overlap_scores) if overlap_scores else 0.5
        return 1.0 - avg_overlap
    
    def _calculate_profile_completeness(self, profile: Dict) -> float:
        """Calculate completeness score for a single profile"""
        fields_to_check = {
            'company_name': 0.2,
            'positioning': 0.2,
            'value_proposition': 0.15,
            'messages': 0.15,
            'colors': 0.1,
            'logo_url': 0.1,
            'personality_traits': 0.1
        }
        
        score = 0.0
        for field, weight in fields_to_check.items():
            if profile.get(field):
                if isinstance(profile[field], list):
                    if profile[field]:  # Non-empty list
                        score += weight
                elif isinstance(profile[field], str):
                    if profile[field].strip():  # Non-empty string
                        score += weight
                else:
                    score += weight
        
        return score
    
    def _list_data_sources(self, profile: Dict) -> List[str]:
        """List data sources used for this profile"""
        sources = []
        
        extraction_method = profile.get('extraction_method', {})
        if extraction_method.get('scraping_method'):
            sources.append(f"Web scraping ({extraction_method['scraping_method']})")
        
        if extraction_method.get('visual_extraction'):
            sources.append("Visual analysis")
        
        if extraction_method.get('ai_analysis'):
            sources.append(f"AI analysis ({extraction_method.get('ai_model', 'GPT-4')})")
        
        if extraction_method.get('structured_data'):
            sources.append("Structured data (JSON-LD)")
        
        return sources if sources else ["Unknown"]
    
    def _summarize_failures(self, failed: List[Dict]) -> List[Dict]:
        """Summarize failure reasons"""
        failure_summary = []
        
        for failure in failed:
            summary = {
                'url': failure.get('url', 'Unknown'),
                'reason': failure.get('error', 'Unknown error'),
                'attempted_methods': failure.get('attempted_methods', []),
                'timestamp': failure.get('timestamp', '')
            }
            failure_summary.append(summary)
        
        return failure_summary
    
    def _create_positioning_map(self, profiles: List[Dict]) -> Dict[str, Any]:
        """Create positioning map based on extracted data"""
        # This would be enhanced with actual positioning analysis
        return {
            'axes': ['Innovation vs Tradition', 'Premium vs Accessible'],
            'positions': [
                {
                    'company': p.get('company_name'),
                    'coordinates': self._calculate_position_coordinates(p)
                } for p in profiles if p.get('company_name')
            ]
        }
    
    def _calculate_position_coordinates(self, profile: Dict) -> Dict[str, float]:
        """Calculate position on competitive map"""
        # Simplified positioning calculation
        positioning_text = (profile.get('positioning', '') + ' ' + 
                          profile.get('value_proposition', '')).lower()
        
        # Innovation vs Tradition (x-axis)
        innovation_score = sum(1 for word in ['innovative', 'cutting-edge', 'modern', 'advanced', 'next-gen'] 
                             if word in positioning_text) * 0.2
        tradition_score = sum(1 for word in ['established', 'trusted', 'proven', 'traditional', 'classic'] 
                            if word in positioning_text) * 0.2
        x = max(-1, min(1, innovation_score - tradition_score))
        
        # Premium vs Accessible (y-axis)
        premium_score = sum(1 for word in ['premium', 'luxury', 'exclusive', 'high-end', 'sophisticated'] 
                          if word in positioning_text) * 0.2
        accessible_score = sum(1 for word in ['affordable', 'accessible', 'simple', 'easy', 'everyone'] 
                             if word in positioning_text) * 0.2
        y = max(-1, min(1, premium_score - accessible_score))
        
        return {'x': x, 'y': y}
    
    def _identify_common_themes(self, profiles: List[Dict]) -> List[Dict]:
        """Identify common themes across brands"""
        from collections import Counter
        
        # Aggregate all messages and positioning statements
        all_text = []
        for profile in profiles:
            all_text.extend(profile.get('messages', []))
            if profile.get('positioning'):
                all_text.append(profile['positioning'])
        
        # Extract meaningful words (simple approach)
        words = []
        for text in all_text:
            words.extend(word.lower() for word in text.split() 
                        if len(word) > 5 and word.isalpha())
        
        # Find common themes
        word_counts = Counter(words)
        common_themes = []
        
        for word, count in word_counts.most_common(10):
            if count >= len(profiles) * 0.5:  # Appears in at least half the brands
                common_themes.append({
                    'theme': word,
                    'frequency': count,
                    'brands_mentioning': self._count_brands_mentioning(word, profiles)
                })
        
        return common_themes
    
    def _count_brands_mentioning(self, word: str, profiles: List[Dict]) -> int:
        """Count how many brands mention a specific word"""
        count = 0
        for profile in profiles:
            brand_text = ' '.join(profile.get('messages', [])) + ' ' + profile.get('positioning', '')
            if word.lower() in brand_text.lower():
                count += 1
        return count
    
    def _identify_differentiation_factors(self, profiles: List[Dict]) -> List[Dict]:
        """Identify unique differentiation factors"""
        factors = []
        
        for profile in profiles:
            unique_terms = self._find_unique_terms(profile, profiles)
            if unique_terms:
                factors.append({
                    'company': profile.get('company_name'),
                    'unique_factors': unique_terms[:5]  # Top 5 unique terms
                })
        
        return factors
    
    def _find_unique_terms(self, profile: Dict, all_profiles: List[Dict]) -> List[str]:
        """Find terms unique to this brand"""
        # Get this brand's terms
        brand_text = ' '.join(profile.get('messages', [])) + ' ' + profile.get('positioning', '')
        brand_terms = set(word.lower() for word in brand_text.split() 
                         if len(word) > 5 and word.isalpha())
        
        # Get all other brands' terms
        other_terms = set()
        for other in all_profiles:
            if other.get('company_name') != profile.get('company_name'):
                other_text = ' '.join(other.get('messages', [])) + ' ' + other.get('positioning', '')
                other_terms.update(word.lower() for word in other_text.split() 
                                 if len(word) > 5 and word.isalpha())
        
        # Find unique terms
        unique = brand_terms - other_terms
        return list(unique)
    
    def _assess_market_maturity(self, profiles: List[Dict]) -> Dict[str, Any]:
        """Assess market maturity based on positioning patterns"""
        maturity_indicators = {
            'high_differentiation': self._calculate_market_differentiation(profiles),
            'established_players': self._count_established_brands(profiles),
            'innovation_focus': self._assess_innovation_focus(profiles),
            'price_competition': self._detect_price_competition(profiles)
        }
        
        # Determine maturity level
        maturity_score = sum(maturity_indicators.values()) / len(maturity_indicators)
        
        if maturity_score > 0.7:
            maturity_level = "mature"
        elif maturity_score > 0.4:
            maturity_level = "growing"
        else:
            maturity_level = "emerging"
        
        return {
            'level': maturity_level,
            'indicators': maturity_indicators,
            'score': maturity_score
        }
    
    def _calculate_market_differentiation(self, profiles: List[Dict]) -> float:
        """Calculate overall market differentiation"""
        if len(profiles) < 2:
            return 0.5
        
        differentiation_scores = []
        for profile in profiles:
            score = self._assess_differentiation(profile, profiles)
            differentiation_scores.append(score)
        
        return statistics.mean(differentiation_scores) if differentiation_scores else 0.0
    
    def _count_established_brands(self, profiles: List[Dict]) -> float:
        """Count brands that appear established"""
        established_count = 0
        
        for profile in profiles:
            text = profile.get('positioning', '') + ' ' + ' '.join(profile.get('messages', []))
            established_words = ['established', 'trusted', 'leading', 'proven', 'experience', 'years']
            
            if any(word in text.lower() for word in established_words):
                established_count += 1
        
        return established_count / len(profiles) if profiles else 0.0
    
    def _assess_innovation_focus(self, profiles: List[Dict]) -> float:
        """Assess focus on innovation across market"""
        innovation_count = 0
        
        for profile in profiles:
            text = profile.get('positioning', '') + ' ' + ' '.join(profile.get('messages', []))
            innovation_words = ['innovative', 'disrupting', 'revolutionary', 'breakthrough', 'cutting-edge']
            
            if any(word in text.lower() for word in innovation_words):
                innovation_count += 1
        
        return innovation_count / len(profiles) if profiles else 0.0
    
    def _detect_price_competition(self, profiles: List[Dict]) -> float:
        """Detect if price is a major competitive factor"""
        price_mentions = 0
        
        for profile in profiles:
            text = profile.get('positioning', '') + ' ' + profile.get('value_proposition', '')
            price_words = ['affordable', 'cost-effective', 'pricing', 'value', 'budget', 'save money']
            
            if any(word in text.lower() for word in price_words):
                price_mentions += 1
        
        return price_mentions / len(profiles) if profiles else 0.0
    
    def _identify_gaps(self, profiles: List[Dict]) -> List[str]:
        """Identify potential market gaps"""
        gaps = []
        
        # Check for underserved segments
        all_audiences = []
        for profile in profiles:
            if profile.get('target_audience'):
                all_audiences.extend(profile['target_audience'])
        
        # Common segments that might be missing
        potential_segments = ['enterprise', 'small business', 'consumer', 'developer', 'non-technical']
        mentioned_segments = ' '.join(all_audiences).lower()
        
        for segment in potential_segments:
            if segment not in mentioned_segments:
                gaps.append(f"Potential underserved segment: {segment}")
        
        # Check for missing value propositions
        all_values = ' '.join(p.get('value_proposition', '') for p in profiles).lower()
        value_gaps = ['automation', 'integration', 'mobile', 'real-time', 'ai-powered']
        
        for value in value_gaps:
            if value not in all_values:
                gaps.append(f"Potential value gap: {value}")
        
        return gaps[:5]  # Top 5 gaps
    
    def _analyze_value_props(self, profiles: List[Dict]) -> List[Dict]:
        """Analyze dominant value propositions"""
        value_categories = {
            'efficiency': ['fast', 'quick', 'efficient', 'streamline', 'automate'],
            'cost_savings': ['save', 'reduce cost', 'affordable', 'budget', 'value'],
            'quality': ['quality', 'premium', 'best', 'superior', 'excellent'],
            'innovation': ['innovative', 'cutting-edge', 'advanced', 'modern', 'next-gen'],
            'simplicity': ['simple', 'easy', 'intuitive', 'user-friendly', 'straightforward']
        }
        
        category_counts = {cat: 0 for cat in value_categories}
        
        for profile in profiles:
            value_prop = profile.get('value_proposition', '').lower()
            for category, keywords in value_categories.items():
                if any(keyword in value_prop for keyword in keywords):
                    category_counts[category] += 1
        
        return [
            {'category': cat, 'count': count, 'percentage': count/len(profiles) if profiles else 0}
            for cat, count in category_counts.items()
            if count > 0
        ]
    
    def _analyze_messaging_patterns(self, profiles: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in brand messaging"""
        message_lengths = []
        message_styles = {'benefit_focused': 0, 'feature_focused': 0, 'emotion_focused': 0}
        
        for profile in profiles:
            messages = profile.get('messages', [])
            for message in messages:
                message_lengths.append(len(message.split()))
                
                # Categorize message style
                lower_msg = message.lower()
                if any(word in lower_msg for word in ['benefit', 'gain', 'achieve', 'improve']):
                    message_styles['benefit_focused'] += 1
                elif any(word in lower_msg for word in ['feature', 'capability', 'function', 'includes']):
                    message_styles['feature_focused'] += 1
                elif any(word in lower_msg for word in ['feel', 'experience', 'love', 'enjoy']):
                    message_styles['emotion_focused'] += 1
        
        return {
            'average_message_length': statistics.mean(message_lengths) if message_lengths else 0,
            'message_style_distribution': message_styles,
            'total_messages_analyzed': len(message_lengths)
        }
    
    def _analyze_audience_overlaps(self, profiles: List[Dict]) -> List[Dict]:
        """Analyze overlapping target audiences"""
        audience_map = {}
        
        for profile in profiles:
            audiences = profile.get('target_audience', [])
            for audience in audiences:
                if audience not in audience_map:
                    audience_map[audience] = []
                audience_map[audience].append(profile.get('company_name'))
        
        overlaps = []
        for audience, companies in audience_map.items():
            if len(companies) > 1:
                overlaps.append({
                    'audience_segment': audience,
                    'competing_brands': companies,
                    'competition_intensity': len(companies)
                })
        
        return sorted(overlaps, key=lambda x: x['competition_intensity'], reverse=True)
    
    def _analyze_tech_mentions(self, profiles: List[Dict]) -> Dict[str, int]:
        """Analyze technology adoption mentions"""
        tech_keywords = {
            'ai': ['ai', 'artificial intelligence', 'machine learning', 'ml'],
            'cloud': ['cloud', 'saas', 'cloud-based', 'hosted'],
            'mobile': ['mobile', 'app', 'ios', 'android'],
            'automation': ['automate', 'automation', 'automated'],
            'integration': ['integrate', 'integration', 'api', 'connect'],
            'analytics': ['analytics', 'insights', 'data', 'metrics']
        }
        
        tech_counts = {tech: 0 for tech in tech_keywords}
        
        for profile in profiles:
            brand_text = (profile.get('positioning', '') + ' ' + 
                         profile.get('value_proposition', '') + ' ' +
                         ' '.join(profile.get('messages', []))).lower()
            
            for tech, keywords in tech_keywords.items():
                if any(keyword in brand_text for keyword in keywords):
                    tech_counts[tech] += 1
        
        return tech_counts
    
    def _identify_positioning_clusters(self, profiles: List[Dict]) -> List[Dict]:
        """Identify clusters of similar positioning"""
        # Simplified clustering based on common positioning themes
        clusters = {
            'performance_focused': [],
            'customer_centric': [],
            'innovation_leaders': [],
            'value_providers': [],
            'niche_specialists': []
        }
        
        cluster_keywords = {
            'performance_focused': ['performance', 'speed', 'efficient', 'powerful', 'results'],
            'customer_centric': ['customer', 'user', 'experience', 'support', 'service'],
            'innovation_leaders': ['innovative', 'pioneer', 'leading', 'advanced', 'breakthrough'],
            'value_providers': ['value', 'affordable', 'cost-effective', 'roi', 'savings'],
            'niche_specialists': ['specialized', 'specific', 'tailored', 'custom', 'unique']
        }
        
        for profile in profiles:
            positioning = profile.get('positioning', '').lower()
            best_cluster = None
            best_score = 0
            
            for cluster, keywords in cluster_keywords.items():
                score = sum(1 for keyword in keywords if keyword in positioning)
                if score > best_score:
                    best_score = score
                    best_cluster = cluster
            
            if best_cluster and best_score > 0:
                clusters[best_cluster].append(profile.get('company_name'))
        
        # Return only non-empty clusters
        return [
            {'cluster': name, 'brands': brands, 'size': len(brands)}
            for name, brands in clusters.items()
            if brands
        ]
    
    def _summarize_methods(self, results: List[Dict]) -> Dict[str, int]:
        """Summarize extraction methods used"""
        method_counts = {}
        
        for result in results:
            methods = result.get('extraction_methods_attempted', [])
            for method in methods:
                method_counts[method] = method_counts.get(method, 0) + 1
        
        return method_counts
    
    def _analyze_failures(self, results: List[Dict]) -> Dict[str, Any]:
        """Analyze failure patterns"""
        failures = [r for r in results if r.get('status') != 'success']
        
        if not failures:
            return {'total_failures': 0}
        
        failure_reasons = {}
        for failure in failures:
            reason = failure.get('error', 'Unknown')
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
        
        return {
            'total_failures': len(failures),
            'failure_reasons': failure_reasons,
            'most_common_failure': max(failure_reasons.items(), key=lambda x: x[1])[0] if failure_reasons else None
        }
    
    def _calculate_duration(self, results: List[Dict]) -> Dict[str, float]:
        """Calculate extraction duration statistics"""
        durations = []
        for result in results:
            if result.get('extraction_duration'):
                durations.append(result['extraction_duration'])
        
        if not durations:
            return {'average': 0, 'total': 0}
        
        return {
            'average': statistics.mean(durations),
            'total': sum(durations),
            'min': min(durations),
            'max': max(durations)
        }
    
    def _count_retries(self, results: List[Dict]) -> Dict[str, int]:
        """Count retry attempts"""
        total_retries = 0
        max_retries = 0
        
        for result in results:
            retries = result.get('retry_count', 0)
            total_retries += retries
            max_retries = max(max_retries, retries)
        
        return {
            'total_retries': total_retries,
            'max_retries_single_brand': max_retries,
            'brands_requiring_retries': len([r for r in results if r.get('retry_count', 0) > 0])
        }
    
    def _assess_data_coverage(self, profiles: List[Dict]) -> Dict[str, float]:
        """Assess coverage of different data types"""
        coverage = {
            'visual_data': len([p for p in profiles if p.get('colors') or p.get('logo_url')]) / len(profiles),
            'positioning_data': len([p for p in profiles if p.get('positioning')]) / len(profiles),
            'messaging_data': len([p for p in profiles if p.get('messages')]) / len(profiles),
            'audience_data': len([p for p in profiles if p.get('target_audience')]) / len(profiles),
            'personality_data': len([p for p in profiles if p.get('personality_traits')]) / len(profiles)
        }
        
        return coverage if profiles else {k: 0.0 for k in coverage.keys()}
    
    def generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """Generate HTML report from analysis data"""
        if report_data.get('status') == 'no_data':
            return self._generate_no_data_html(report_data)
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Brand Analysis Report - {datetime.now().strftime('%Y-%m-%d')}</title>
            <style>
                {self._get_report_styles()}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Brand Competitive Analysis Report</h1>
                    <p class="timestamp">Generated: {report_data['timestamp']}</p>
                </header>
                
                {self._generate_summary_section(report_data['summary'])}
                {self._generate_quality_metrics_section(report_data['quality_metrics'])}
                {self._generate_brand_profiles_section(report_data['brand_profiles'])}
                {self._generate_landscape_section(report_data['competitive_landscape'])}
                {self._generate_insights_section(report_data['market_insights'])}
                {self._generate_extraction_details_section(report_data['extraction_details'])}
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _get_report_styles(self) -> str:
        """Get CSS styles for the report"""
        return """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        h1 {
            margin: 0 0 10px 0;
            color: #2c3e50;
        }
        
        .timestamp {
            color: #7f8c8d;
            margin: 0;
        }
        
        .section {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .section h2 {
            color: #2c3e50;
            margin-top: 0;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .metric-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
            margin: 10px 0;
        }
        
        .metric-label {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        
        .brand-profile {
            border: 1px solid #ecf0f1;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .brand-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .brand-logo {
            width: 60px;
            height: 60px;
            margin-right: 20px;
            object-fit: contain;
        }
        
        .brand-name {
            font-size: 1.5em;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .data-quality {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            margin-left: 10px;
        }
        
        .quality-high {
            background: #d4edda;
            color: #155724;
        }
        
        .quality-medium {
            background: #fff3cd;
            color: #856404;
        }
        
        .quality-low {
            background: #f8d7da;
            color: #721c24;
        }
        
        .positioning-statement {
            font-style: italic;
            color: #555;
            margin: 15px 0;
            padding: 15px;
            background: #f8f9fa;
            border-left: 4px solid #3498db;
        }
        
        .messages-list {
            list-style: none;
            padding: 0;
        }
        
        .messages-list li {
            padding: 8px 0;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .color-palette {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        
        .color-swatch {
            width: 40px;
            height: 40px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        
        .insights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .insight-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }
        
        .insight-title {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .warning {
            background: #fff3cd;
            border: 1px solid #ffeeba;
            border-radius: 4px;
            padding: 15px;
            margin: 20px 0;
        }
        
        .error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            padding: 15px;
            margin: 20px 0;
        }
        """
    
    def _generate_no_data_html(self, report_data: Dict[str, Any]) -> str:
        """Generate HTML for when no data could be extracted"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Brand Analysis Report - No Data</title>
            <style>{self._get_report_styles()}</style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Brand Competitive Analysis Report</h1>
                    <p class="timestamp">Generated: {report_data['timestamp']}</p>
                </header>
                
                <div class="section error">
                    <h2>Analysis Failed</h2>
                    <p>{report_data['message']}</p>
                    <p>Attempted to analyze {report_data['attempted_count']} brand(s).</p>
                    
                    <h3>Failure Details:</h3>
                    <ul>
                        {self._format_failures_html(report_data.get('failures', []))}
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _format_failures_html(self, failures: List[Dict]) -> str:
        """Format failure details as HTML"""
        html_items = []
        for failure in failures:
            html_items.append(f"""
                <li>
                    <strong>{failure.get('url', 'Unknown URL')}</strong>
                    <br>Reason: {failure.get('reason', 'Unknown')}
                    <br>Attempted methods: {', '.join(failure.get('attempted_methods', []))}
                </li>
            """)
        return ''.join(html_items)
    
    def _generate_summary_section(self, summary: Dict[str, Any]) -> str:
        """Generate summary section HTML"""
        return f"""
        <div class="section">
            <h2>Executive Summary</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Total Brands</div>
                    <div class="metric-value">{summary['total_brands_analyzed']}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Success Rate</div>
                    <div class="metric-value">{summary['extraction_rate']:.0%}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Data Completeness</div>
                    <div class="metric-value">{summary['data_completeness']:.0%}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Analysis Depth</div>
                    <div class="metric-value">{summary['analysis_depth'].title()}</div>
                </div>
            </div>
            
            {self._format_industries(summary.get('industries_detected', []))}
        </div>
        """
    
    def _format_industries(self, industries: List[str]) -> str:
        """Format detected industries"""
        if not industries:
            return ""
        
        return f"""
        <div style="margin-top: 20px;">
            <strong>Industries Detected:</strong> {', '.join(industries)}
        </div>
        """
    
    def _generate_quality_metrics_section(self, metrics: Dict[str, Any]) -> str:
        """Generate data quality metrics section"""
        return f"""
        <div class="section">
            <h2>Data Quality Metrics</h2>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Avg Completeness</div>
                    <div class="metric-value">{metrics['average_completeness']:.0%}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">High Quality</div>
                    <div class="metric-value">{metrics['high_quality_profiles']}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Low Quality</div>
                    <div class="metric-value">{metrics['low_quality_profiles']}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Avg Confidence</div>
                    <div class="metric-value">{metrics['average_confidence']:.0%}</div>
                </div>
            </div>
        </div>
        """
    
    def _generate_brand_profiles_section(self, profiles: List[Dict]) -> str:
        """Generate brand profiles section"""
        profiles_html = []
        
        for profile in profiles:
            quality_class = self._get_quality_class(profile['data_quality']['completeness_score'])
            
            profile_html = f"""
            <div class="brand-profile">
                <div class="brand-header">
                    {self._format_logo(profile.get('logo_url'))}
                    <div>
                        <span class="brand-name">{profile.get('company_name', 'Unknown')}</span>
                        <span class="data-quality {quality_class}">
                            {profile['data_quality']['completeness_score']:.0%} Complete
                        </span>
                    </div>
                </div>
                
                {self._format_positioning(profile.get('positioning'))}
                {self._format_value_prop(profile.get('value_proposition'))}
                {self._format_messages(profile.get('messages', []))}
                {self._format_colors(profile.get('colors', []))}
                {self._format_metrics(profile.get('comparative_metrics', {}))}
            </div>
            """
            profiles_html.append(profile_html)
        
        return f"""
        <div class="section">
            <h2>Brand Profiles</h2>
            {''.join(profiles_html)}
        </div>
        """
    
    def _get_quality_class(self, score: float) -> str:
        """Get CSS class for quality score"""
        if score >= 0.8:
            return "quality-high"
        elif score >= 0.5:
            return "quality-medium"
        else:
            return "quality-low"
    
    def _format_logo(self, logo_url: Optional[str]) -> str:
        """Format logo HTML"""
        if logo_url:
            return f'<img src="{logo_url}" class="brand-logo" alt="Brand logo">'
        return '<div class="brand-logo" style="background: #ecf0f1; display: flex; align-items: center; justify-content: center; color: #7f8c8d;">No Logo</div>'
    
    def _format_positioning(self, positioning: Optional[str]) -> str:
        """Format positioning statement"""
        if not positioning:
            return ""
        return f'<div class="positioning-statement">{positioning}</div>'
    
    def _format_value_prop(self, value_prop: Optional[str]) -> str:
        """Format value proposition"""
        if not value_prop:
            return ""
        return f'<div><strong>Value Proposition:</strong> {value_prop}</div>'
    
    def _format_messages(self, messages: List[str]) -> str:
        """Format brand messages"""
        if not messages:
            return ""
        
        messages_html = ''.join(f'<li>{msg}</li>' for msg in messages[:5])
        return f"""
        <div style="margin-top: 15px;">
            <strong>Key Messages:</strong>
            <ul class="messages-list">{messages_html}</ul>
        </div>
        """
    
    def _format_colors(self, colors: List[str]) -> str:
        """Format color palette"""
        if not colors:
            return ""
        
        swatches = ''.join(f'<div class="color-swatch" style="background: {color};" title="{color}"></div>' 
                          for color in colors[:5])
        return f"""
        <div style="margin-top: 15px;">
            <strong>Brand Colors:</strong>
            <div class="color-palette">{swatches}</div>
        </div>
        """
    
    def _format_metrics(self, metrics: Dict[str, float]) -> str:
        """Format comparative metrics"""
        if not metrics:
            return ""
        
        return f"""
        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #ecf0f1;">
            <strong>Comparative Metrics:</strong>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 10px;">
                <div>
                    <div style="color: #7f8c8d; font-size: 0.9em;">Positioning Clarity</div>
                    <div style="font-weight: bold;">{metrics.get('positioning_clarity', 0):.0%}</div>
                </div>
                <div>
                    <div style="color: #7f8c8d; font-size: 0.9em;">Message Consistency</div>
                    <div style="font-weight: bold;">{metrics.get('message_consistency', 0):.0%}</div>
                </div>
                <div>
                    <div style="color: #7f8c8d; font-size: 0.9em;">Value Prop Strength</div>
                    <div style="font-weight: bold;">{metrics.get('value_prop_strength', 0):.0%}</div>
                </div>
                <div>
                    <div style="color: #7f8c8d; font-size: 0.9em;">Differentiation</div>
                    <div style="font-weight: bold;">{metrics.get('brand_differentiation', 0):.0%}</div>
                </div>
            </div>
        </div>
        """
    
    def _generate_landscape_section(self, landscape: Dict[str, Any]) -> str:
        """Generate competitive landscape section"""
        if landscape.get('status') == 'insufficient_data':
            return f"""
            <div class="section">
                <h2>Competitive Landscape</h2>
                <div class="warning">{landscape['message']}</div>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2>Competitive Landscape</h2>
            
            {self._format_positioning_map(landscape.get('positioning_map', {}))}
            {self._format_common_themes(landscape.get('common_themes', []))}
            {self._format_market_gaps(landscape.get('competitive_gaps', []))}
            {self._format_maturity(landscape.get('market_maturity_indicators', {}))}
        </div>
        """
    
    def _format_positioning_map(self, pos_map: Dict[str, Any]) -> str:
        """Format positioning map (simplified text version)"""
        if not pos_map.get('positions'):
            return ""
        
        positions_html = []
        for pos in pos_map['positions']:
            x_label = "Innovative" if pos['coordinates']['x'] > 0 else "Traditional"
            y_label = "Premium" if pos['coordinates']['y'] > 0 else "Accessible"
            positions_html.append(f"<li><strong>{pos['company']}</strong>: {x_label}, {y_label}</li>")
        
        return f"""
        <div style="margin-bottom: 20px;">
            <h3>Brand Positioning</h3>
            <ul>{''.join(positions_html)}</ul>
        </div>
        """
    
    def _format_common_themes(self, themes: List[Dict]) -> str:
        """Format common themes"""
        if not themes:
            return ""
        
        themes_html = []
        for theme in themes[:5]:
            themes_html.append(f"""
                <li>
                    <strong>{theme['theme'].title()}</strong> - 
                    mentioned by {theme['brands_mentioning']} brands
                </li>
            """)
        
        return f"""
        <div style="margin-bottom: 20px;">
            <h3>Common Market Themes</h3>
            <ul>{''.join(themes_html)}</ul>
        </div>
        """
    
    def _format_market_gaps(self, gaps: List[str]) -> str:
        """Format market gaps"""
        if not gaps:
            return ""
        
        gaps_html = ''.join(f'<li>{gap}</li>' for gap in gaps)
        
        return f"""
        <div style="margin-bottom: 20px;">
            <h3>Potential Market Gaps</h3>
            <ul>{gaps_html}</ul>
        </div>
        """
    
    def _format_maturity(self, maturity: Dict[str, Any]) -> str:
        """Format market maturity assessment"""
        if not maturity:
            return ""
        
        return f"""
        <div>
            <h3>Market Maturity: {maturity.get('level', 'Unknown').title()}</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
                <div>Differentiation Level: {maturity['indicators'].get('high_differentiation', 0):.0%}</div>
                <div>Established Players: {maturity['indicators'].get('established_players', 0):.0%}</div>
                <div>Innovation Focus: {maturity['indicators'].get('innovation_focus', 0):.0%}</div>
                <div>Price Competition: {maturity['indicators'].get('price_competition', 0):.0%}</div>
            </div>
        </div>
        """
    
    def _generate_insights_section(self, insights: Dict[str, Any]) -> str:
        """Generate market insights section"""
        return f"""
        <div class="section">
            <h2>Market Insights</h2>
            <div class="insights-grid">
                {self._format_value_prop_insights(insights.get('dominant_value_propositions', []))}
                {self._format_messaging_insights(insights.get('messaging_patterns', {}))}
                {self._format_tech_insights(insights.get('technology_adoption', {}))}
                {self._format_cluster_insights(insights.get('market_positioning_clusters', []))}
            </div>
        </div>
        """
    
    def _format_value_prop_insights(self, value_props: List[Dict]) -> str:
        """Format value proposition insights"""
        if not value_props:
            return ""
        
        items = []
        for prop in value_props:
            items.append(f"<li>{prop['category'].replace('_', ' ').title()}: {prop['percentage']:.0%}</li>")
        
        return f"""
        <div class="insight-card">
            <div class="insight-title">Value Proposition Focus</div>
            <ul>{{''.join(items)}}</ul>
        </div>
        """
    
    def _format_messaging_insights(self, patterns: Dict[str, Any]) -> str:
        """Format messaging pattern insights"""
        if not patterns:
            return ""
        
        return f"""
        <div class="insight-card">
            <div class="insight-title">Messaging Patterns</div>
            <div>Average message length: {patterns.get('average_message_length', 0):.0f} words</div>
            <div>Messages analyzed: {patterns.get('total_messages_analyzed', 0)}</div>
        </div>
        """
    
    def _format_tech_insights(self, tech_adoption: Dict[str, int]) -> str:
        """Format technology adoption insights"""
        if not tech_adoption:
            return ""
        
        items = []
        for tech, count in sorted(tech_adoption.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                items.append(f"<li>{tech.upper()}: {count} brands</li>")
        
        return f"""
        <div class="insight-card">
            <div class="insight-title">Technology Mentions</div>
            <ul>{''.join(items)}</ul>
        </div>
        """
    
    def _format_cluster_insights(self, clusters: List[Dict]) -> str:
        """Format positioning cluster insights"""
        if not clusters:
            return ""
        
        items = []
        for cluster in clusters:
            items.append(f"<li>{cluster['cluster'].replace('_', ' ').title()}: {cluster['size']} brands</li>")
        
        return f"""
        <div class="insight-card">
            <div class="insight-title">Positioning Clusters</div>
            <ul>{''.join(items)}</ul>
        </div>
        """
    
    def _generate_extraction_details_section(self, details: Dict[str, Any]) -> str:
        """Generate extraction details section"""
        return f"""
        <div class="section">
            <h2>Extraction Details</h2>
            
            <h3>Methods Used</h3>
            <ul>
                {self._format_methods(details.get('extraction_methods_used', {}))}
            </ul>
            
            <h3>Performance</h3>
            <div>
                Average extraction time: {details.get('extraction_duration', {}).get('average', 0):.1f}s<br>
                Total retries: {details.get('retry_attempts', {}).get('total_retries', 0)}
            </div>
            
            {self._format_failure_analysis(details.get('failure_analysis', {}))}
        </div>
        """
    
    def _format_methods(self, methods: Dict[str, int]) -> str:
        """Format extraction methods"""
        items = []
        for method, count in methods.items():
            items.append(f"<li>{method}: used {count} times</li>")
        return ''.join(items)
    
    def _format_failure_analysis(self, failures: Dict[str, Any]) -> str:
        """Format failure analysis"""
        if failures.get('total_failures', 0) == 0:
            return "<p>No extraction failures encountered.</p>"
        
        reasons_html = []
        for reason, count in failures.get('failure_reasons', {}).items():
            reasons_html.append(f"<li>{reason}: {count} occurrences</li>")
        
        return f"""
        <h3>Failure Analysis</h3>
        <div>
            Total failures: {failures['total_failures']}<br>
            Most common failure: {failures.get('most_common_failure', 'N/A')}
        </div>
        <ul>{''.join(reasons_html)}</ul>
        """
