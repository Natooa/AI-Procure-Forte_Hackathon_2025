package kz.aihackathon.aiprocure.repository.tender;

import kz.aihackathon.aiprocure.model.Tender;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TenderRepository extends JpaRepository<Tender, Long> {

}
