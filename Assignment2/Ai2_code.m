clear all;
T = [0.7 0.3; 0.3 0.7];%Dynamic model
umb = [1 1 0 1 1]; %evidence
O = [0.1 0;0 0.8]; %Observation model
O(:,:,2) = [0.9 0; 0 0.2]; %Observation model
fv = zeros(2,6);%Forward messages init
fv(:,1) = [0.5; 0.5];
for i=2:6 %Forward
    fv(:,i) = (O(:,:,umb(i-1)+1)*T.'*fv(:,i-1))/sum(O(:,:,umb(i-1)+1)*T.'*fv(:,i-1)); %Eq. 15.12
end

sv = zeros(2,6);%Smoothed messages init
b = zeros(2,6);%Backward message init
b(:,6) = [1; 1];

for i=6:-1:2 %Normalize and Backward
    sv(:,i)=(fv(:,i).*b(:,i))/sum(fv(:,i).*b(:,i));%Fig 15.4
    b(:,i-1) = T*O(:,:,umb(i-1)+1)*b(:,i); %Eq. 15.13
end
fv, sv, b %print

%====Plot====%
hold on;
title('Forward');
plot(fv(1,2:6));
plot(fv(2,2:6));
plot(sv(1,2:6));
plot(sv(2,2:6));
legend('Probability of rain[Forward]', 'Probability of no rain[Forward]','Probability of rain[Forward-Backward]', 'Probability of no rain[Forward-Backward]');
xlabel('Day');
ylabel('Probability');
