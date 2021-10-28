# CI_CD_WEEK7
## CI/CD Pipeline with azure devops 

Welcome To azure devops!
![image](https://user-images.githubusercontent.com/71599740/139231659-f2e624e9-9b26-431d-91e8-84a2e4dd297a.png) 

There are 2 pipelines:

CI pipeline - creating an artifact and uploading to Artifactory
CD Pipeline - Downloading the LTS artifact from artifactory and running the new app.



## STEPS:
1. Configure two agents: my-pool and Prod-pool One for the CI and one for the CD - https://www.youtube.com/watch?v=psa8xfJ0-zI&ab_channel=Raaviblog
2. run the agent as a systemd service: https://docs.microsoft.com/en-us/azure/devops/pipelines/agents/v2-linux?view=azure-devops
3. Import a project repository
4. Create a new artifacts feed
5. Created the build pipeline using the visual editor
6. Selected the imported repository as build sources - GITHUB
7. Selected the "Empty Job" template
8. Configured the pipeline to run in the my-pool (CI)
9. Configure CI Trigger: Enable continuous integration   => If you would like to make a change to the app push the new commit to the master branch and the pipelines will do the rest
10. create these tasks:
![image](https://user-images.githubusercontent.com/71599740/139233845-698bdbe4-c297-4792-96c8-522a4a367bc0.png)
![image](https://user-images.githubusercontent.com/71599740/139233912-a8cb9cca-84ef-4b09-95c5-ed17bbf2cd68.png)
![image](https://user-images.githubusercontent.com/71599740/139233954-589d771a-327a-4360-ae28-b3ba018c878c.png)
![image](https://user-images.githubusercontent.com/71599740/139233973-58544222-45be-4ad5-81b9-53891409823e.png)

11. Create a release pipeline definition -Click on "add a new artifact"
12. Configure the artifact trigger: Continuous deployment trigger: Enabled
13. Access to the environment configuration: </br>
 ![image](https://user-images.githubusercontent.com/71599740/139234710-0491138e-be7d-4f43-88d6-89b1ab2a0ada.png)
 ![image](https://user-images.githubusercontent.com/71599740/139236417-9a0682e6-a2d9-4b12-81cb-0c2156db9918.png)
![image](https://user-images.githubusercontent.com/71599740/139236540-e65c591b-72e7-4896-a995-c73a101836ac.png)

