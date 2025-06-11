package core;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.*;
import java.util.stream.Collectors;

public class GenerateData {
    public static void main(String[] args) throws IOException, InterruptedException {
        List<String> userInfoLines=getDataFromFile("user_info.txt");
        List<CellInfo> cellLocLines=getDataFromFile("cell_loc.txt").stream().map(x->{
            String [] cellLocLine_split=x.split("\\|");
            CellInfo cellinfo=new CellInfo();
            cellinfo.cell=cellLocLine_split[0];
            cellinfo.lat=cellLocLine_split[1];
            cellinfo.lot=cellLocLine_split[2];

            return cellinfo;
        }).sorted(Comparator.comparingLong(x->Long.parseLong(x.cell))).collect(Collectors.toList());


        for(int i=0;i<cellLocLines.size();i++){
            cellLocLines.get(i).index=i;

        }
        Map<Integer,CellInfo> cellindex_cell_Map=cellLocLines.stream().collect(Collectors.toMap(x->x.index, x->x));
        Map<String,Integer> cell_cellindex_Map=cellLocLines.stream().collect(Collectors.toMap(x->x.cell, x->x.index));


        Map<String, String> userStatus = new HashMap<>();

        Random r=new Random();

            while(true){
                //随机获取一个用户的imsi
                String ranUserline=userInfoLines.get(r.nextInt(userInfoLines.size()));

                String [] ranUserline_split=ranUserline.split("\\|");
                String imsi=ranUserline_split[0];

                int lastIndex=cell_cellindex_Map.getOrDefault(userStatus.get(imsi),r.nextInt(cellLocLines.size())) ;

                int step=r.nextInt(7)-3;

                if(step>0){
                    int[] chose={lastIndex+step<cellLocLines.size()?lastIndex+step:lastIndex-step,lastIndex-step>0?lastIndex-step:lastIndex+step};
                    int nextIndex=chose[r.nextInt(2)];


                    CellInfo nextcell=cellindex_cell_Map.get(nextIndex);

                    userStatus.put(imsi,nextcell.cell);
                    //生成进入基站时间
                    //生成进入基站时间
                    long currTime=System.currentTimeMillis();

                    String data=imsi+"|"+nextcell.cell+"|"+nextcell.lat+"|"+nextcell.lot+"|"+currTime;


                    System.out.println(data);


                }


                Thread.sleep(100);



            }



    }

    static public void old() throws IOException, InterruptedException{
        List<String> userInfoLines=getDataFromFile("user_info.txt");
        List<String> cellLocLines=getDataFromFile("cell_loc.txt");

        Random r=new Random();
        while(true){
            //随机获取一个用户的imsi
            String ranUserline=userInfoLines.get(r.nextInt(userInfoLines.size()));
            String [] ranUserline_split=ranUserline.split("\\|");
            String imsi=ranUserline_split[0];

            //随机获取一个小区cell标识
            String cellLocLine=cellLocLines.get(r.nextInt(cellLocLines.size()));
            String [] cellLocLine_split=cellLocLine.split("\\|");
            String cell=cellLocLine_split[0];
            String lat=cellLocLine_split[1];
            String lot=cellLocLine_split[2];


            //生成进入基站时间
            long currTime=System.currentTimeMillis();

            String data=imsi+"|"+cell+"|"+lat+"|"+lot+"|"+currTime;

            System.out.println(data);
            Thread.sleep(1000);

        }
    }
    private static List<String> getDataFromFile(String filePath) throws IOException {
        List<String> list= new ArrayList<>();

        try(BufferedReader br=new BufferedReader(new InputStreamReader(GenerateData.class.getClassLoader().getResourceAsStream(filePath)))){
            String line;
            while((line=br.readLine())!=null){
                list.add(line);
            }
        }
        return list;
    }
}
class CellInfo{
    public String cell;
    public String lat;
    public String lot;
    public int index;
    public CellInfo(){

    }
    public CellInfo(int index){
        this.index=index;
    }
    @Override
    public String toString() {
        return cell+"|"+lat+"|"+lot+"|"+index;
    }
}