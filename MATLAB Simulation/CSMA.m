
%% Init
clear all
ts = 1;
num_node = 4;
backoffs = 2.^(3:5)-1;
Sendingnode = 0;
t_series = 1:ts:300;
for d = 1:num_node
    node(d).CD = 0;
    node(d).backoff = 0;
    node(d).backofftime = 0;
    node(d).fail = 0;
    node(d).waitime = 0;
    node(d).ack = 0;
    node(d).acktime = 0;
    node(d).sendtime = 9;
    node(d).sending = 0;
    node(d).recv = 0;
    node(d).difs = 0;
    node(d).interference = 0;%Success transmit or not
    node(d).bfindex = 1;
    node(d).prevtrans = 0;%Previous transmit successful or not
    node(d).previous = '';
    [nodeshow(d).backoff,nodeshow(d).ack ,nodeshow(d).sending,nodeshow(d).occupied,nodeshow(d).difs,nodeshow(d).sifs,nodeshow(d).recv] = deal(zeros(1,length(t_series)+1));
end
DIFS = 1;
SIFS = 1;
ACK = 1;
maxACK = 2;
EIFS = SIFS + ACK + DIFS;
Carrier = 0;
Carriers = zeros(1,length(t_series)+1);
est = zeros(2,length(t_series)+1);
Sendingcount = node(d).sendtime;%Count down for major sender
From = 0;
fail = 0;
recv_num = 0;
from1 = 0;
from2  = 0;
inters=0;%Interference of node 1 due to MAC
ifinter = 0;
sendcount=0;
s_count = 0;
cds = zeros(1,length(t_series));
[spds,acks,wins,winsact] = deal([]);
for t = t_series
    for d = 2:num_node
        %%   State trasnfer
        %node(d).previous
        %node(d).waitime
        if node(d).CD == 0
            if  node(d).waitime == 0%End of the previous pro cess or being occupied
                if strcmp(node(d).previous,'occupied') ||t == 1 ||strcmp(node(d).previous,'ack')
                    
                    if t == 1
                        node(d).waitime = randi([1,num_node*3]);
                    else
                        node(d).waitime = DIFS;
                    end
                    node(d).previous = 'difs';
                    nodeshow(d).difs(t) = 1;
                elseif strcmp(node(d).previous,'difs')
                    if node(d).backofftime==0 %No cached backoff
                        [node(d).waitime,node(d).backofftime]= deal(randi([1 backoffs(node(d).bfindex)]));
                        if d==2
                            winsact = [winsact node(2).waitime];
                             wins = [wins node(2).bfindex];
                        end
                    else
                        node(d).waitime = node(d).backofftime;
                    end
                    nodeshow(d).backoff(t) = 1;
                    %sprintf("BF time %d, %d",d,node(d).waitime)
                    node(d).previous = 'backoff';
                elseif strcmp(node(d).previous,'backoff')%Send!
                    node(d).waitime = node(d).sendtime;
                    node(d).previous ='send';
                    nodeshow(d).sending(t) = 1;
                    if d==2
                    sendcount = sendcount + 1;
                    end
                    ifinter = 0;
                end
            end
            
        else %CD, then occupied
            if strcmp(node(d).previous,'send')
                node(d).interference = 1;
                if ifinter==0 && d == 2
                    inters = inters+1;
                    ifinter = 1;
                end
            else
                node(d).previous = 'occupied';
                nodeshow(d).occupied(t) = 1;
                node(d).waitime = 0;
            end
        end%End 0 CD
        %% Ack
        if strcmp(node(d).previous,'send')&& node(d).waitime == 0 %Not affected by CD
            if 1%node(d).sendtime == 4
                lossrate = 1;
            end
            channeloss = rand(1)>lossrate;
            if node(d).interference || channeloss%Interference
                if node(d).bfindex ~= length(backoffs)%Add window
                    node(d).bfindex =node(d).bfindex + 1;
                end
                node(d).interference = 0;
                node(d).waitime  = maxACK;
                if node(d).prevtrans == -1%Down speed
                    node(d).sendtime = 9;%modspd(node(d).sendtime,-1);
                    node(d).prevtrans = 0;
                else
                    node(d).prevtrans = -1;
                end
                if d==2
                    acks = [acks 0];
                end
            else%Successful transmit
                node(d).waitime  = DIFS;
                node(1).recv = 1;
                From = d;
                node(d).bfindex = 1;
                recv_num = recv_num+1;
                if node(d).prevtrans == 1
                    node(d).sendtime = 9;%modspd(node(d).sendtime,1);
                    node(d).prevtrans = 0;
                else
                    node(d).prevtrans = 1;
                end
                if d == 2
                     acks = [acks 1];
                     s_count = s_count + 1;
                end
            end
            if d == 2
            spds = [spds (1/node(2).sendtime)*4-1];
            end
            node(d).previous = 'ack';
            nodeshow(d).ack(t) = 1;
        end
        %% Time step
        if node(d).waitime ~= 0
            node(d).waitime = node(d).waitime - 1;
            if node(d).backofftime ~= 0 && strcmp(node(d).previous,'backoff')%Back off count down
                node(d).backofftime = node(d).backofftime - 1;
            end
        end
        if node(d).waitime > 0%Plot graph
            [nodeshow(d).backoff(t+1),nodeshow(d).ack(t+1) ,nodeshow(d).sending(t+1),nodeshow(d).occupied(t+1),nodeshow(d).difs(t+1)] = deal(nodeshow(d).backoff(t),nodeshow(d).ack(t) ,nodeshow(d).sending(t),nodeshow(d).occupied(t),nodeshow(d).difs(t));
        end
        % est(d-1,t) = strcmp(node(d).previous,'send');
    end% end of d node
    %% End of previous process, no need CD
    %% Major sender
    if 0%Sendingcount && Sendingnode
        Sendingcount = Sendingcount - 1;
    else
        Sendingcount = node(d).sendtime+SIFS;%Count down for major sender
        Sendingnode = 0;%Finish one send
    end
    %% CD search
    Carrier = 0;
    carrier = zeros(1,num_node);
    for d = 2:num_node
        if strcmp(node(d).previous,'send')%More than one node is sending
            carrier(d) = 1;
        end
    end
    for d = 2:num_node%Skip major sender
        node(d).CD=(sum(carrier(setdiff(1:num_node,d)))~=0);
        %node(d).CD = Carrier;% * (~strcmp(node(d).previous,'send'));
        %est(d-1,t) = ~strcmp(node(d).previous,'send')*Carrier;
    end
    cds(t) = node(2).CD;
    %Carriers(t) = Carrier;% Global CD
    %% Receiver
    for r = 1:1%Receiver
        if node(r).recv == 1
            nodeshow(d).recv(t) = 1;
            node(r).recv  = 0;
            node(r).waitime = ACK; %Sending ack
            %sprintf("receive from %d",From)
            if From == 2
                from1 = from1 +1 ;
            elseif From == 3
                from2 = from2 +1;
            end
        end
    end
end
%% Plot
["Recv",recv_num, "From1",from1,"From2",from2,"MAC inter from 1",inters/sendcount, "MAC/all loss",(sendcount-s_count)/sendcount]
if 0
    for s = 2:num_node
        subplot(num_node,1,s-1)
        hold on
        bar(nodeshow(s).backoff,1,'k')
        bar(nodeshow(s).ack,1,'y')
        bar(nodeshow(s).sending,1,'g')
        bar(nodeshow(s).occupied,1,'r')
        bar(nodeshow(s).difs,1,'c')
        bar(nodeshow(s).sifs,1,'m')
        title("Sending Node:",s)
    end
    
    legend("Backoff","Ack","Send+SIFS","Occupied","DIFS")
    subplot(4,1,4)
    bar(nodeshow(d).recv)
    legend("Receive")
    title("Receiver Node")
    %subplot(4,1,3)
    %bar(est(2,:),1)
end
%bar(spds,1)
%bar(cds,1)
%bar(acks,1)
%bar(backoffs(wins),1,'y')
%hold on
%plot(winsact,'LineWidth',2)
sum(acks)/length(acks)