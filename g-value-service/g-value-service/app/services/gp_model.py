import torch
import gpytorch
import numpy as np
from typing import Dict, Any, Tuple
import random

class GValuePredictor:
    """Gaussian Process model for G-value prediction."""
    
    def __init__(self):
        self.model = None
        self.likelihood = None
        self.is_trained = False
        
    def _extract_features(self, features: Dict[str, Any]) -> torch.Tensor:
        """Extract and normalize features for the model."""
        # Convert features to a tensor
        feature_vector = []
        
        # Location-based features (simplified)
        pickup = features.get("pickup_location", "")
        dropoff = features.get("dropoff_location", "")
        
        # Simple feature extraction (in production, use proper geocoding)
        pickup_hash = hash(pickup) % 1000 / 1000.0
        dropoff_hash = hash(dropoff) % 1000 / 1000.0
        
        # Time-based features
        eta = features.get("eta", 0) / 60.0  # Normalize to hours
        time_of_day = features.get("time_of_day", 12) / 24.0  # Normalize to 0-1
        day_of_week = features.get("day_of_week", 1) / 7.0  # Normalize to 0-1
        
        # Distance estimation (simplified)
        distance = abs(pickup_hash - dropoff_hash) * 10  # Mock distance
        
        feature_vector = [
            pickup_hash,
            dropoff_hash,
            eta,
            time_of_day,
            day_of_week,
            distance
        ]
        
        return torch.tensor(feature_vector, dtype=torch.float32).unsqueeze(0)
    
    def _generate_mock_training_data(self, n_samples: int = 100) -> Tuple[torch.Tensor, torch.Tensor]:
        """Generate mock training data for the GP model."""
        # Generate random features
        X = torch.randn(n_samples, 6)  # 6 features
        
        # Generate mock G-values with some structure
        # Higher G-values for certain combinations
        g_values = []
        for i in range(n_samples):
            # Base G-value influenced by features
            base_g = 0.3 + 0.4 * torch.sigmoid(X[i, 0] + X[i, 1])  # Location influence
            time_bonus = 0.1 * torch.sin(X[i, 2] * np.pi)  # Time influence
            distance_penalty = -0.05 * X[i, 5]  # Distance penalty
            
            g_value = base_g + time_bonus + distance_penalty + 0.1 * torch.randn(1)
            g_value = torch.clamp(g_value, 0.1, 1.0)  # Clamp between 0.1 and 1.0
            g_values.append(g_value)
        
        y = torch.cat(g_values)
        return X, y
    
    def train_model(self):
        """Train the Gaussian Process model with mock data."""
        try:
            # Generate training data
            X_train, y_train = self._generate_mock_training_data(100)
            
            # Define the GP model
            class ExactGPModel(gpytorch.models.ExactGP):
                def __init__(self, train_x, train_y, likelihood):
                    super(ExactGPModel, self).__init__(train_x, train_y, likelihood)
                    self.mean_module = gpytorch.means.ConstantMean()
                    self.covar_module = gpytorch.kernels.ScaleKernel(
                        gpytorch.kernels.RBFKernel()
                    )
                
                def forward(self, x):
                    mean_x = self.mean_module(x)
                    covar_x = self.covar_module(x)
                    return gpytorch.distributions.MultivariateNormal(mean_x, covar_x)
            
            # Initialize likelihood and model
            self.likelihood = gpytorch.likelihoods.GaussianLikelihood()
            self.model = ExactGPModel(X_train, y_train, self.likelihood)
            
            # Set to training mode
            self.model.train()
            self.likelihood.train()
            
            # Use Adam optimizer
            optimizer = torch.optim.Adam(self.model.parameters(), lr=0.1)
            
            # Loss function
            mll = gpytorch.mlls.ExactMarginalLogLikelihood(self.likelihood, self.model)
            
            # Training loop
            for i in range(50):  # Reduced iterations for faster startup
                optimizer.zero_grad()
                output = self.model(X_train)
                loss = -mll(output, y_train)
                loss.backward()
                optimizer.step()
            
            self.is_trained = True
            print("GP model trained successfully")
            
        except Exception as e:
            print(f"Error training GP model: {e}")
            self.is_trained = False
    
    def predict(self, features: Dict[str, Any]) -> Tuple[float, float]:
        """Make G-value prediction."""
        try:
            if not self.is_trained:
                self.train_model()
            
            if not self.is_trained:
                # Fallback to mock prediction
                return self._mock_prediction(features)
            
            # Extract features
            X = self._extract_features(features)
            
            # Set to evaluation mode
            self.model.eval()
            self.likelihood.eval()
            
            # Make prediction
            with torch.no_grad(), gpytorch.settings.fast_pred_var():
                observed_pred = self.likelihood(self.model(X))
                mean = observed_pred.mean.item()
                variance = observed_pred.variance.item()
            
            # Ensure reasonable bounds
            mean = max(0.1, min(1.0, mean))
            variance = max(0.01, min(0.5, variance))
            
            return mean, variance
            
        except Exception as e:
            print(f"Error in GP prediction: {e}")
            return self._mock_prediction(features)
    
    def _mock_prediction(self, features: Dict[str, Any]) -> Tuple[float, float]:
        """Generate mock G-value prediction when model fails."""
        # Use features to generate deterministic but varied predictions
        pickup = features.get("pickup_location", "")
        dropoff = features.get("dropoff_location", "")
        eta = features.get("eta", 15)
        
        # Generate deterministic but varied values
        seed = hash(f"{pickup}{dropoff}{eta}") % 1000
        random.seed(seed)
        
        # Base G-value influenced by ETA (shorter ETA = higher G-value)
        base_g = 0.4 + 0.4 * (1.0 - min(eta / 60.0, 1.0))  # 0.4 to 0.8 range
        
        # Add some noise
        noise = random.gauss(0, 0.1)
        g_mean = max(0.1, min(1.0, base_g + noise))
        
        # Variance based on uncertainty
        g_var = 0.05 + random.uniform(0, 0.15)  # 0.05 to 0.2 range
        
        return g_mean, g_var

# Global instance
gp_predictor = GValuePredictor()
