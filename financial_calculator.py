"""Financial calculator for farm profit and break-even analysis"""
from typing import Dict, List
from datetime import datetime

class FinancialCalculator:
    """Calculate farm profitability, expenses, and break-even points"""
    
    def __init__(self):
        # Default cost estimates (INR per acre)
        self.default_costs = {
            "seed": {"Wheat": 2500, "Rice": 3000, "Corn": 2800, "Soybeans": 3500, "Cotton": 4000},
            "fertilizer": {"Wheat": 4000, "Rice": 5000, "Corn": 4500, "Soybeans": 3800, "Cotton": 5500},
            "pesticide": {"Wheat": 2000, "Rice": 2500, "Corn": 2200, "Soybeans": 2300, "Cotton": 3500},
            "labor": {"Wheat": 8000, "Rice": 10000, "Corn": 8500, "Soybeans": 7500, "Cotton": 12000},
            "irrigation": {"Wheat": 3000, "Rice": 6000, "Corn": 4000, "Soybeans": 3500, "Cotton": 5000},
            "equipment": {"Wheat": 2000, "Rice": 2500, "Corn": 2200, "Soybeans": 2000, "Cotton": 3000},
        }
    
    def calculate_total_cost(self, crop: str, area_acres: float, custom_costs: Dict = None) -> Dict:
        """Calculate total farming costs"""
        if custom_costs:
            costs = custom_costs
        else:
            costs = {
                "seed": self.default_costs["seed"].get(crop, 3000),
                "fertilizer": self.default_costs["fertilizer"].get(crop, 4500),
                "pesticide": self.default_costs["pesticide"].get(crop, 2500),
                "labor": self.default_costs["labor"].get(crop, 9000),
                "irrigation": self.default_costs["irrigation"].get(crop, 4000),
                "equipment": self.default_costs["equipment"].get(crop, 2500),
                "other": 1500,
            }
        
        total_per_acre = sum(costs.values())
        total_cost = total_per_acre * area_acres
        
        return {
            "costs_per_acre": costs,
            "total_per_acre": total_per_acre,
            "total_cost": total_cost,
            "area_acres": area_acres,
            "breakdown_percent": {k: (v/total_per_acre)*100 for k, v in costs.items()}
        }
    
    def calculate_profit(self, total_cost: float, yield_quantity: float, 
                        selling_price: float) -> Dict:
        """Calculate profit/loss from farming"""
        revenue = yield_quantity * selling_price
        profit = revenue - total_cost
        profit_percent = (profit / total_cost) * 100 if total_cost > 0 else 0
        roi = (profit / total_cost) * 100 if total_cost > 0 else 0
        
        return {
            "total_cost": total_cost,
            "revenue": revenue,
            "profit": profit,
            "profit_percent": profit_percent,
            "roi": roi,
            "status": "profit" if profit > 0 else "loss"
        }
    
    def calculate_breakeven(self, total_cost: float, yield_quantity: float) -> Dict:
        """Calculate break-even price"""
        if yield_quantity <= 0:
            return {"error": "Yield quantity must be greater than 0"}
        
        breakeven_price = total_cost / yield_quantity
        
        # Calculate prices for different profit margins
        profit_margins = [10, 20, 30, 50]
        target_prices = {}
        for margin in profit_margins:
            target_price = breakeven_price * (1 + margin/100)
            target_prices[f"{margin}%_profit"] = target_price
        
        return {
            "breakeven_price": breakeven_price,
            "yield_quantity": yield_quantity,
            "total_cost": total_cost,
            "target_prices": target_prices
        }
    
    def estimate_yield(self, crop: str, area_acres: float, 
                      weather_quality: str = "good") -> Dict:
        """Estimate crop yield based on area and conditions"""
        # Average yields (quintals per acre)
        base_yields = {
            "Wheat": 15, "Rice": 18, "Corn": 20, "Soybeans": 12,
            "Cotton": 8, "Sugarcane": 300, "Potatoes": 100,
            "Tomatoes": 150, "Onions": 120, "Groundnut": 10
        }
        
        # Weather quality multipliers
        multipliers = {
            "excellent": 1.2,
            "good": 1.0,
            "average": 0.85,
            "poor": 0.6,
            "very_poor": 0.4
        }
        
        base_yield = base_yields.get(crop, 10)
        multiplier = multipliers.get(weather_quality, 1.0)
        
        yield_per_acre = base_yield * multiplier
        total_yield = yield_per_acre * area_acres
        
        return {
            "crop": crop,
            "area_acres": area_acres,
            "yield_per_acre_quintals": yield_per_acre,
            "total_yield_quintals": total_yield,
            "weather_quality": weather_quality,
            "multiplier": multiplier
        }
    
    def calculate_loan_requirement(self, total_cost: float, own_capital: float,
                                   interest_rate: float = 7.0, 
                                   loan_period_months: int = 6) -> Dict:
        """Calculate loan requirements and repayment"""
        loan_amount = max(0, total_cost - own_capital)
        
        if loan_amount <= 0:
            return {
                "loan_required": False,
                "loan_amount": 0,
                "message": "Sufficient own capital available"
            }
        
        # Simple interest calculation
        interest = (loan_amount * interest_rate * loan_period_months) / (12 * 100)
        total_repayment = loan_amount + interest
        monthly_emi = total_repayment / loan_period_months
        
        return {
            "loan_required": True,
            "loan_amount": loan_amount,
            "own_capital": own_capital,
            "interest_rate": interest_rate,
            "loan_period_months": loan_period_months,
            "interest_amount": interest,
            "total_repayment": total_repayment,
            "monthly_emi": monthly_emi
        }
    
    def compare_scenarios(self, crop: str, area_acres: float, 
                         price_scenarios: List[float]) -> List[Dict]:
        """Compare profit under different price scenarios"""
        cost_data = self.calculate_total_cost(crop, area_acres)
        yield_data = self.estimate_yield(crop, area_acres)
        
        scenarios = []
        for price in price_scenarios:
            profit_data = self.calculate_profit(
                cost_data["total_cost"],
                yield_data["total_yield_quintals"],
                price
            )
            scenarios.append({
                "selling_price": price,
                "revenue": profit_data["revenue"],
                "profit": profit_data["profit"],
                "roi": profit_data["roi"],
                "status": profit_data["status"]
            })
        
        return scenarios
