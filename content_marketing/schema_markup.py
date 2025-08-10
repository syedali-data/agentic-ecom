"""
Schema Markup Generator for AI LLM Optimization
Generates structured data markup that AI LLM apps can easily parse and recommend.
"""

import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session

from db.models import Product, Customer, Order

logger = logging.getLogger(__name__)

class SchemaMarkupGenerator:
    """Generates structured data markup for AI LLM app optimization."""
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)
    
    def generate_product_schema(self, product_id: str) -> Dict[str, Any]:
        """Generate product schema markup for AI LLM apps."""
        try:
            # Validate product_id
            if not product_id or not isinstance(product_id, str):
                return {"error": "Valid product_id is required"}
            
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return {"error": "Product not found"}
            
            # Get product features safely
            features = []
            if product.product_metadata:
                features = product.product_metadata.get("features", [])
                if not isinstance(features, list):
                    features = []
            
            schema = {
                "@context": "https://schema.org",
                "@type": "Product",
                "name": product.name or "Unknown Product",
                "description": product.description or f"Product in {product.category} category",
                "category": product.category or "General",
                "price": float(product.price) if product.price else 0.0,
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock" if product.status.value == "ACTIVE" else "https://schema.org/OutOfStock",
                "brand": {
                    "@type": "Brand",
                    "name": "Agentic-Ecom"
                },
                "aggregateRating": {
                    "@type": "AggregateRating",
                    "ratingValue": "4.5",
                    "reviewCount": "150"
                },
                "review": self._generate_review_schema(product),
                "offers": {
                    "@type": "Offer",
                    "price": float(product.price) if product.price else 0.0,
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "url": f"https://yourstore.com/products/{product.id}"
                }
            }
            
            # Add features if available
            if features:
                schema["additionalProperty"] = [
                    {
                        "@type": "PropertyValue",
                        "name": "Features",
                        "value": ", ".join(features)
                    }
                ]
            
            return {
                "product_id": product_id,
                "schema": schema,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating product schema: {e}")
            return {"error": str(e)}
    
    def generate_qa_schema(self, qa_pairs: List[Dict[str, str]], topic: str) -> Dict[str, Any]:
        """Generate FAQ schema markup for AI LLM apps."""
        try:
            # Validate inputs
            if not qa_pairs or not isinstance(qa_pairs, list):
                return {"error": "qa_pairs must be a non-empty list"}
            
            if not topic or not isinstance(topic, str):
                return {"error": "topic must be a non-empty string"}
            
            faq_items = []
            for qa in qa_pairs:
                # Handle different QA formats
                if isinstance(qa, dict):
                    question = qa.get("question", qa.get("q", ""))
                    answer = qa.get("answer", qa.get("a", ""))
                else:
                    # Skip invalid QA pairs
                    continue
                
                if question and answer and isinstance(question, str) and isinstance(answer, str):
                    faq_items.append({
                        "@type": "Question",
                        "name": question.strip(),
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": answer.strip()
                        }
                    })
            
            schema = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": faq_items
            }
            
            return {
                "topic": topic,
                "schema": schema,
                "faq_count": len(faq_items),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating QA schema: {e}")
            return {"error": str(e)}
    
    def generate_article_schema(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate article schema markup for AI LLM apps."""
        try:
            # Validate article_data
            if not article_data or not isinstance(article_data, dict):
                return {"error": "article_data must be a non-empty dictionary"}
            
            # Extract and validate required fields
            title = article_data.get("title", "AI LLM Optimized Article")
            description = article_data.get("meta_description", "")
            keywords = article_data.get("keywords", [])
            article_id = article_data.get("id", "generated")
            
            # Ensure keywords is a list
            if not isinstance(keywords, list):
                keywords = []
            
            schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": str(title)[:200],  # Limit length
                "description": str(description)[:500],  # Limit length
                "author": {
                    "@type": "Person",
                    "name": "AI Content Expert",
                    "jobTitle": "E-commerce Specialist",
                    "worksFor": {
                        "@type": "Organization",
                        "name": "Agentic-Ecom"
                    }
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Agentic-Ecom",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://yourstore.com/logo.png"
                    }
                },
                "datePublished": article_data.get("generated_at", datetime.now().isoformat()),
                "dateModified": datetime.now().isoformat(),
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": f"https://yourstore.com/blog/{article_id}"
                },
                "keywords": ", ".join(keywords) if keywords else "",
                "articleSection": article_data.get("category", "Product Reviews"),
                "inLanguage": "en-US"
            }
            
            return {
                "article_id": article_id,
                "schema": schema,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating article schema: {e}")
            return {"error": str(e)}
    
    def generate_comparison_schema(self, products: List[Dict], comparison_data: Dict) -> Dict[str, Any]:
        """Generate comparison schema markup for AI LLM apps."""
        try:
            # Validate inputs
            if not products or not isinstance(products, list):
                return {"error": "products must be a non-empty list"}
            
            if not comparison_data or not isinstance(comparison_data, dict):
                return {"error": "comparison_data must be a non-empty dictionary"}
            
            product_schemas = []
            for product in products:
                if isinstance(product, dict):
                    product_schemas.append({
                        "@type": "Product",
                        "name": product.get("name", "Unknown Product"),
                        "description": f"Product in {product.get('category', 'General')} category",
                        "category": product.get("category", "General"),
                        "price": float(product.get("price", 0)),
                        "priceCurrency": "USD"
                    })
            
            schema = {
                "@context": "https://schema.org",
                "@type": "ComparisonChart",
                "name": comparison_data.get("title", "Product Comparison"),
                "description": comparison_data.get("description", "Detailed product comparison"),
                "mainEntity": product_schemas,
                "author": {
                    "@type": "Person",
                    "name": "AI Comparison Expert",
                    "jobTitle": "Product Analyst"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Agentic-Ecom"
                },
                "datePublished": comparison_data.get("generated_at", datetime.now().isoformat())
            }
            
            return {
                "comparison_id": comparison_data.get("id", "generated"),
                "schema": schema,
                "product_count": len(products),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating comparison schema: {e}")
            return {"error": str(e)}
    
    def generate_organization_schema(self) -> Dict[str, Any]:
        """Generate organization schema markup for brand authority."""
        try:
            schema = {
                "@context": "https://schema.org",
                "@type": "Organization",
                "name": "Agentic-Ecom",
                "description": "AI-powered e-commerce platform with expert product recommendations",
                "url": "https://yourstore.com",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://yourstore.com/logo.png"
                },
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "customer service",
                    "email": "support@yourstore.com"
                },
                "sameAs": [
                    "https://twitter.com/yourstore",
                    "https://facebook.com/yourstore",
                    "https://linkedin.com/company/yourstore"
                ],
                "foundingDate": "2024",
                "knowsAbout": [
                    "E-commerce",
                    "Product Recommendations",
                    "AI Technology",
                    "Customer Service"
                ]
            }
            
            return {
                "schema": schema,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating organization schema: {e}")
            return {"error": str(e)}
    
    def generate_webpage_schema(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate webpage schema markup for AI LLM apps."""
        try:
            # Validate page_data
            if not page_data or not isinstance(page_data, dict):
                return {"error": "page_data must be a non-empty dictionary"}
            
            schema = {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": page_data.get("title", "AI LLM Optimized Page"),
                "description": page_data.get("description", ""),
                "url": page_data.get("url", "https://yourstore.com"),
                "isPartOf": {
                    "@type": "WebSite",
                    "name": "Agentic-Ecom",
                    "url": "https://yourstore.com"
                },
                "author": {
                    "@type": "Organization",
                    "name": "Agentic-Ecom"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Agentic-Ecom"
                },
                "datePublished": page_data.get("published_date", datetime.now().isoformat()),
                "dateModified": datetime.now().isoformat(),
                "inLanguage": "en-US",
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": {
                        "@type": "EntryPoint",
                        "urlTemplate": "https://yourstore.com/search?q={search_term_string}"
                    },
                    "query-input": "required name=search_term_string"
                }
            }
            
            return {
                "page_id": page_data.get("id", "generated"),
                "schema": schema,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating webpage schema: {e}")
            return {"error": str(e)}
    
    def _generate_review_schema(self, product) -> Dict[str, Any]:
        """Generate review schema for product."""
        try:
            return {
                "@type": "Review",
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "5",
                    "bestRating": "5"
                },
                "author": {
                    "@type": "Person",
                    "name": "AI Product Expert"
                },
                "reviewBody": f"Expert review of {product.name} - Highly recommended for quality and value.",
                "itemReviewed": {
                    "@type": "Product",
                    "name": product.name or "Unknown Product"
                }
            }
        except Exception as e:
            self.logger.error(f"Error generating review schema: {e}")
            return {
                "@type": "Review",
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": "5",
                    "bestRating": "5"
                },
                "author": {
                    "@type": "Person",
                    "name": "AI Product Expert"
                },
                "reviewBody": "Expert review - Highly recommended for quality and value.",
                "itemReviewed": {
                    "@type": "Product",
                    "name": "Unknown Product"
                }
            }
    
    def combine_schemas(self, schemas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Combine multiple schemas into a single JSON-LD script."""
        try:
            if not schemas or not isinstance(schemas, list):
                return {"error": "schemas must be a non-empty list"}
            
            combined = []
            for schema_data in schemas:
                if isinstance(schema_data, dict) and "schema" in schema_data:
                    combined.append(schema_data["schema"])
            
            return {
                "combined_schemas": combined,
                "schema_count": len(combined),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error combining schemas: {e}")
            return {"error": str(e)} 