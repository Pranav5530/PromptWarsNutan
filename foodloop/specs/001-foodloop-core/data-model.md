# Data Model Specification: FoodLoop

## 1. Firestore Operational Collections

### `users` Collection
- `id` (string, PK / Firebase UID)
- `email` (string)
- `displayName` (string)
- `role` (enum: `donor`, `ngo`, `volunteer`, `admin`)
- `phoneMasked` (string, e.g. `+91-XXXXX-12345`)
- `phoneRaw` (string, stored in restricted subcollection `users/{id}/private/security`)
- `organizationName` (string, optional)
- `location`:
  - `latitude` (float)
  - `longitude` (float)
  - `addressText` (string)
  - `city` (string)
- `createdAt` (timestamp)
- `updatedAt` (timestamp)

### `ngos` (Extended metadata for NGOs)
- `userId` (string, ref `users.id`)
- `capacityMeals` (integer, e.g. 150)
- `dietaryPolicy` (enum: `veg_only`, `all`, `halal`)
- `operatingHours`: `{ open: "08:00", close: "23:00" }`
- `active` (boolean)
- `currentDeficit` (integer)

### `volunteers` (Extended metadata for Volunteers)
- `userId` (string, ref `users.id`)
- `isAvailable` (boolean)
- `transportMode` (enum: `bike`, `two_wheeler`, `car`, `on_foot`)
- `currentLocation`: `{ latitude: float, longitude: float }`
- `lastActiveAt` (timestamp)

### `listings` Collection
- `id` (string, UUID)
- `donorId` (string, ref `users.id`)
- `donorName` (string)
- `donorLocation`: `{ latitude: float, longitude: float, addressMasked: string }`
- `photoUrl` (string)
- `foodName` (string)
- `category` (enum: `cooked_meal`, `bakery`, `raw_produce`, `packaged`)
- `estimatedKg` (float)
- `mealCount` (integer)
- `dietaryType` (enum: `vegetarian`, `vegan`, `non_vegetarian`, `jain`)
- `allergens` (array of string: `dairy`, `nuts`, `gluten`, etc.)
- `prepTimestamp` (timestamp)
- `safeConsumeWindowHours` (integer)
- `safeConsumeBy` (timestamp)
- `storageCondition` (enum: `hot_held`, `room_temp`, `refrigerated`)
- `safetyStatus`:
  - `verdict` (enum: `Safe`, `Risky`, `Rejected`)
  - `ruleViolations` (array of string)
  - `aiExplanation` (string)
  - `evaluatedAt` (timestamp)
- `donorConfirmed` (boolean)
- `status` (enum: `draft`, `evaluating_safety`, `safe`, `risky`, `rejected`, `matching`, `matched`, `dispatching`, `assigned`, `in_transit`, `delivered`, `expired`, `cancelled`)
- `createdAt` (timestamp)
- `updatedAt` (timestamp)

### `matches` Collection
- `id` (string, UUID)
- `listingId` (string, ref `listings.id`)
- `rankedCandidates`: array of objects:
  - `ngoId` (string)
  - `ngoName` (string)
  - `score` (float: 0.0 - 1.0)
  - `distanceKm` (float)
  - `reasoning` (string)
- `selectedNgoId` (string)
- `offeredAt` (timestamp)
- `expiresAt` (timestamp, offeredAt + 120s)
- `ngoResponse` (enum: `pending`, `accepted`, `declined`, `timed_out`)
- `respondedAt` (timestamp)

### `dispatches` Collection
- `id` (string, UUID)
- `listingId` (string, ref `listings.id`)
- `ngoId` (string, ref `users.id`)
- `volunteerId` (string, ref `users.id`)
- `status` (enum: `assigned`, `en_route_pickup`, `picked_up`, `en_route_delivery`, `delivered`, `cancelled`)
- `route`:
  - `distanceMeters` (integer)
  - `etaMinutes` (integer)
  - `directionsUrl` (string)
- `pickupProofUrl` (string, optional)
- `deliveryProofPhotoUrl` (string, optional)
- `completedAt` (timestamp)

---

## 2. BigQuery Analytics Schema (`foodloop_analytics`)

### Table: `listing_lifecycle_events`
- `event_id` STRING (REQUIRED)
- `listing_id` STRING (REQUIRED)
- `event_type` STRING (REQUIRED: `created`, `safety_checked`, `matched`, `dispatched`, `delivered`, `expired`)
- `timestamp` TIMESTAMP (REQUIRED)
- `donor_id` STRING
- `donor_city` STRING
- `donor_area` STRING
- `food_category` STRING
- `kg_rescued` FLOAT64
- `meals_served` INT64
- `co2_saved_kg` FLOAT64 (calibrated at 2.5 kg CO2e per kg food rescued)
- `match_latency_sec` FLOAT64
- `pickup_latency_min` FLOAT64
- `safety_verdict` STRING

### Table: `surplus_forecast_predictions` (BigQuery ML Output)
- `forecast_date` DATE
- `area_name` STRING
- `hour_of_day` INT64
- `predicted_surplus_kg` FLOAT64
- `confidence_score` FLOAT64
