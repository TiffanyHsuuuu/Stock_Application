package stock.application.stock;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;


public class Stock {
    private int stock_number;
    private Integer index;
    private float price;
    private float priceChange;
    private float percentChange;
    private int volume;
    private int averageVolume;
    private float peRatio;
    private int marketCap;

    public Stock(int stock_number, float price, int volume) {
        this.stock_number = stock_number;
        this.price = price;
        this.volume = volume;
    }

    public int getStock_number() {
        return stock_number;
    }

    public void setStock_number(int stock_number) {
        this.stock_number = stock_number;
    }

    public Integer getIndex() {
        return index;
    }

    public void setIndex(int index) {
        this.index = index;
    }

    public float getPrice() {
        return price;
    }

    public void setPrice(float price) {
        this.price = price;
    }

    public float getPriceChange() {
        return priceChange;
    }

    public void setPriceChange(float priceChange) {
        this.priceChange = priceChange;
    }

    public float getPercentChange() {
        return percentChange;
    }

    public void setPercentChange(float percentChange) {
        this.percentChange = percentChange;
    }

    public int getVolume() {
        return volume;
    }

    public void setVolume(int volume) {
        this.volume = volume;
    }

    public int getAverageVolume() {
        return averageVolume;
    }

    public void setAverageVolume(int averageVolume) {
        this.averageVolume = averageVolume;
    }

    public float getPeRatio() {
        return peRatio;
    }

    public void setPeRatio(float peRatio) {
        this.peRatio = peRatio;
    }

    public int getMarketCap() {
        return marketCap;
    }

    public void setMarketCap(int marketCap) {
        this.marketCap = marketCap;
    }

    @Override
    public String toString() {
        return "Stock{" +
                "price=" + price +
                ", priceChange=" + priceChange +
                ", percentChange=" + percentChange +
                ", volume=" + volume +
                ", averageVolume=" + averageVolume +
                ", peRatio=" + peRatio +
                ", marketCap=" + marketCap +
                '}';
    }
}
