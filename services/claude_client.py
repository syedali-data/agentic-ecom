import os
import logging
from typing import Dict, Any, Optional, List
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class ClaudeClient:
    """Abstraction layer for Claude API calls with error handling and rate limiting"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = Anthropic(api_key=self.api_key)
        self.default_model = "claude-3-5-sonnet-20241022"
        self.default_max_tokens = 500
        self.default_temperature = 0.5
        
        logger.info("Claude client initialized successfully")
    
    def generate_response(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_prompt: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response using Claude
        
        Args:
            prompt: The user prompt
            model: Claude model to use
            max_tokens: Maximum tokens to generate
            temperature: Creativity level (0.0 to 1.0)
            system_prompt: System prompt for context
            metadata: Additional metadata for logging
            
        Returns:
            Dict containing response text and metadata
        """
        try:
            model = model or self.default_model
            max_tokens = max_tokens or self.default_max_tokens
            temperature = temperature or self.default_temperature
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages
            )
            
            result = {
                "text": response.content[0].text,
                "model": model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "metadata": metadata or {}
            }
            
            logger.info(f"Claude response generated successfully. Tokens: {result['usage']}")
            return result
            
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}")
            return {
                "text": f"Error generating response: {str(e)}",
                "error": True,
                "metadata": metadata or {}
            }
    
    def analyze_text(
        self,
        text: str,
        analysis_type: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze text for specific purposes (fraud, compliance, etc.)
        
        Args:
            text: Text to analyze
            analysis_type: Type of analysis (fraud, compliance, sentiment, etc.)
            context: Additional context for analysis
            
        Returns:
            Analysis results
        """
        analysis_prompts = {
            "fraud": "Analyze this text for potential fraud indicators. Return SAFE, SUSPICIOUS, or HIGH_RISK with reasoning.",
            "compliance": "Check this text for compliance violations. Return COMPLIANT or VIOLATION with details.",
            "sentiment": "Analyze the sentiment of this text. Return POSITIVE, NEUTRAL, or NEGATIVE with confidence score.",
            "quality": "Assess the quality of this text. Return HIGH, MEDIUM, or LOW with reasoning."
        }
        
        prompt = analysis_prompts.get(analysis_type, "Analyze this text.")
        if context:
            prompt = f"{prompt}\n\nContext: {context}\n\nText: {text}"
        else:
            prompt = f"{prompt}\n\nText: {text}"
        
        return self.generate_response(
            prompt=prompt,
            max_tokens=200,
            temperature=0.3,
            metadata={"analysis_type": analysis_type}
        )
    
    def generate_support_response(
        self,
        customer_message: str,
        order_context: Optional[Dict[str, Any]] = None,
        tone: str = "professional"
    ) -> Dict[str, Any]:
        """
        Generate customer support response
        
        Args:
            customer_message: Customer's message
            order_context: Order information if available
            tone: Response tone (professional, friendly, empathetic)
            
        Returns:
            Generated support response
        """
        system_prompt = f"""You are a professional e-commerce customer support agent. 
        Respond in a {tone} tone. Be helpful, clear, and empathetic.
        Keep responses concise (2-3 sentences maximum)."""
        
        context_info = ""
        if order_context:
            context_info = f"\nOrder Context: {order_context}"
        
        prompt = f"""Customer Message: {customer_message}{context_info}

        Please provide a helpful response that:
        1. Acknowledges their concern
        2. Provides clear, actionable information
        3. Maintains a positive tone
        4. Follows e-commerce best practices"""
        
        return self.generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=150,
            temperature=0.7,
            metadata={"support_response": True, "tone": tone}
        )
    
    def optimize_process(
        self,
        process_data: Dict[str, Any],
        optimization_goal: str
    ) -> Dict[str, Any]:
        """
        Optimize business processes using Claude's analytical capabilities
        
        Args:
            process_data: Process data to analyze
            optimization_goal: Goal for optimization (efficiency, cost, quality)
            
        Returns:
            Optimization recommendations
        """
        prompt = f"""Analyze this business process data and provide optimization recommendations:

        Process Data: {process_data}
        Optimization Goal: {optimization_goal}

        Focus on:
        1. Identifying bottlenecks and inefficiencies
        2. Cost optimization opportunities
        3. Quality improvement suggestions
        4. Specific, actionable recommendations

        Provide 3-5 specific recommendations with brief explanations."""
        
        return self.generate_response(
            prompt=prompt,
            max_tokens=300,
            temperature=0.5,
            metadata={"process_optimization": True, "goal": optimization_goal}
        )

# Global instance for easy access
claude_client = ClaudeClient() 