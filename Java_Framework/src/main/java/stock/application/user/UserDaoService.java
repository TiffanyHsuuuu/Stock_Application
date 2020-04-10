package stock.application.user;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.RestController;
import stock.application.stock.Stock;

import javax.validation.constraints.Size;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

@Component
public class UserDaoService {
    private static List<User> user_lst = new ArrayList<>();
    private static int id = 3;

    static {
        user_lst.add(new User(1, "Lara", "lalala", new ArrayList<Stock>()));
        user_lst.add(new User(2, "Nathalie", "nanana", new ArrayList<Stock>()));
        user_lst.add(new User(3, "Azza", "zazaza", new ArrayList<Stock>()));
    }

    public List<User> findAllUsers() {
        return user_lst;
    }
    public User save(User user) {
        if(user.getId() == null)
            user.setId(++ id);
        user_lst.add(user);
        return user;
    }
    public User findUser(int id) {
        for(User user: user_lst)
            if(user.getId()==id)
                return user;
        return null;
    }
    public User deleteUser(int id) {
        Iterator<User> iterator = user_lst.iterator();
        while(iterator.hasNext()) {
            User user = iterator.next();
            if(user.getId() == id) {
                iterator.remove();
                return user;
            }
        }
        return null;
    }
}
