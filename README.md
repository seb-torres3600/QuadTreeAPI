# QuadTreeAPI

## Summary
- A simple flask api intented to pull "boundary" data from a postgresql database 

-  Currently only has one endpoint reading shape data given constraints

## Endpoint Structures

### /get_zones/table_name/constraints
- get_zones = endpoint name
- table_name = table name to pull from
- constraints = comma seperated float values representing coordinate points (x1, y1, x2, y2) 

## Point Constraints Description
- (x1, y1) = lower left coordinate point of boundary
- (x2, y2) = upper right coordinate point of boundary

## Example API Call

```
curl http://localhost:8080/get_zones/data/0.0,0.0,10.0,10.0
```