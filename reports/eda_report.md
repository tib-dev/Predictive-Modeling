# EDA Report

## Dataset Shape
(1000098, 52)

## Columns and Types

- **UnderwrittenCoverID**: int64
- **PolicyID**: int64
- **TransactionMonth**: object
- **IsVATRegistered**: bool
- **Citizenship**: object
- **LegalType**: object
- **Title**: object
- **Language**: object
- **Bank**: object
- **AccountType**: object
- **MaritalStatus**: object
- **Gender**: object
- **Country**: object
- **Province**: object
- **PostalCode**: int64
- **MainCrestaZone**: object
- **SubCrestaZone**: object
- **ItemType**: object
- **mmcode**: float64
- **VehicleType**: object
- **RegistrationYear**: int64
- **make**: object
- **Model**: object
- **Cylinders**: float64
- **cubiccapacity**: float64
- **kilowatts**: float64
- **bodytype**: object
- **NumberOfDoors**: float64
- **VehicleIntroDate**: object
- **CustomValueEstimate**: float64
- **AlarmImmobiliser**: object
- **TrackingDevice**: object
- **CapitalOutstanding**: object
- **NewVehicle**: object
- **WrittenOff**: object
- **Rebuilt**: object
- **Converted**: object
- **CrossBorder**: object
- **NumberOfVehiclesInFleet**: float64
- **SumInsured**: float64
- **TermFrequency**: object
- **CalculatedPremiumPerTerm**: float64
- **ExcessSelected**: object
- **CoverCategory**: object
- **CoverType**: object
- **CoverGroup**: object
- **Section**: object
- **Product**: object
- **StatutoryClass**: object
- **StatutoryRiskType**: object
- **TotalPremium**: float64
- **TotalClaims**: float64

## Top 20 Missing Values

| Column | % Missing |
|--------|-----------|
| NumberOfVehiclesInFleet | 100.00% |
| CrossBorder | 99.93% |
| CustomValueEstimate | 77.96% |
| Rebuilt | 64.18% |
| Converted | 64.18% |
| WrittenOff | 64.18% |
| NewVehicle | 15.33% |
| Bank | 14.59% |
| AccountType | 4.02% |
| Gender | 0.95% |
| MaritalStatus | 0.83% |
| VehicleType | 0.06% |
| make | 0.06% |
| mmcode | 0.06% |
| Model | 0.06% |
| Cylinders | 0.06% |
| bodytype | 0.06% |
| kilowatts | 0.06% |
| NumberOfDoors | 0.06% |
| VehicleIntroDate | 0.06% |

## Duplicates
0


## Outliers

| Column | Outlier Count |
|--------|---------------|
| UnderwrittenCoverID | 5717 |
| PolicyID | 31232 |
| PostalCode | 8149 |
| mmcode | 241512 |
| RegistrationYear | 7482 |
| Cylinders | 34262 |
| cubiccapacity | 56939 |
| kilowatts | 2175 |
| NumberOfDoors | 106708 |
| CustomValueEstimate | 1785 |
| NumberOfVehiclesInFleet | 0 |
| SumInsured | 104294 |
| CalculatedPremiumPerTerm | 175508 |
| TotalPremium | 209042 |
| TotalClaims | 2793 |
| LossRatio | 2643 |